from datetime import datetime

import json
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, CreateView, UpdateView

from core.pos.mixins import ExistsCompanyMixin, ValidatePermissionRequiredMixin
from core.pos.models import Product, Shopping, ShoppingDetail
from core.processes.forms import ProductionForm
from core.processes.models import production, detail_production, ProductionShopping
from core.reports.forms import ReportForm


class ProductionListView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'production/list.html'
    permission_required = 'view_production'

    def calc_efficiency(self, lista_de_diccionarios):
        # Crear un diccionario para almacenar los valores por clave
        valores_por_clave = {}

        for i in lista_de_diccionarios:
            # Si existe el valor el el diccionario
            if i['category'] in valores_por_clave:
                # valores_por_clave[i['branch__name']][0].append(int(i['status']))
                valores_por_clave[i['category']] += i['cant']
            else:
                # Si no existe el valor en el diccionario
                valores_por_clave[i['category']] = i['cant']

        # Verificamos si existe un sub producto
        if not 'SP' in valores_por_clave:
            # Si no existe se valida en 0
            SP = 0
        else:
            SP = valores_por_clave['SP']

        PF = valores_por_clave['PF']

        # Calculo de la eficiencia
        efficiency = (PF * 100) / (SP + PF)

        data = {'efficiency': efficiency, 'PF': PF}

        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = production.objects.select_related()
                if len(start_date) and len(end_date) and request.user.is_superuser:
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                elif len(start_date) and len(end_date) and not request.user.is_superuser:
                    queryset = queryset.filter(
                        Q(user_id=request.user.id) & Q(date_joined__range=[start_date, end_date]))
                elif not len(start_date) and not len(end_date) and not request.user.is_superuser:
                    queryset = queryset.filter(user_id=request.user.id)

                for i in queryset:
                    data.append(i.toLIST())
            elif action == 'search_products_detail':
                data = []
                for i in detail_production.objects.filter(production_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'change_status':
                now = datetime.now()
                today = str(now.date())

                # Leemos en formato JSON los porductos a modificar
                products = json.loads(request.POST['products'])

                # Mandamos a calcular la eficiencia y la cantidad de PRODUCTO FINAL
                calc = self.calc_efficiency(products)

                # Seleccionamos el objeto de la produccion
                prod = production.objects.get(id=products[0]['production'])
                prod.status = True
                prod.efficiency = float(calc['efficiency'])
                # Al momento de cambiar el status automaticmanete la fecha del fin del proceso de guarda la del dia
                # que cambiamos el status
                prod.date_end_process = today
                prod.save()

                # Eliminamos Los productos existentes en la tabla de detalle de produccion
                prod.detail_production_set.all().delete()

                # Seleccionamos las compras de materia prima para sumar y dividir con la cantidad de sacos
                # de lls productos finales y asi sacar el costo de produccion de cada saco
                productionShopping = prod.productionshopping_set.all()

                cost = 0.00

                for pshopping in productionShopping:
                    cost += float(pshopping.shopping_cart.total)

                totalCost = cost / float(calc['PF'])

                for p in products:
                    detail = detail_production()
                    detail.production_id = prod.id
                    detail.product_id = int(p['product_id'])
                    detail.cant = int(p['cant'])
                    # parte para agregar la cantidad producida al stock
                    detail.product.stock = int(p['cant'])
                    # agregamos el costo de cada unos de los productos
                    detail.product.cost = totalCost
                    detail.product.save()
                    detail.save()
            elif action == 'search_raw_materials':
                p = ProductionShopping.objects.select_related().filter(production_id=request.POST['id'])
                shopping = []
                total = 0.00

                for ps in p:
                    total += float(ps.subtotal)
                    product = f'{ps.product.code} {ps.product.name} {ps.product.brand.name} {ps.product.um}'
                    supplier = f'{ps.shopping_cart.invoice_number} - {ps.shopping_cart.supplier.name}'
                    shopping.append({'id': ps.id, 'supplier': supplier, 'product': product,
                                     'price': ps.price, 'cant': ps.cant, 'subtotal': ps.subtotal})
                shopping.append(
                    {'id': '---------', 'supplier': '---------', 'product': '---------', 'price': '',
                     'cant': '---------', 'subtotal': total})

                data = shopping
            elif action == 'delete':
                prod = production.objects.get(id=request.POST['id'])
                if prod.status:
                    pass
                else:
                    prod.delete()
            else:
                data['error'] = 'No se ha encontrado el action'
        except Exception as e:
            # print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de producción'
        context['create_url'] = reverse_lazy('production_add')
        context['list_url'] = reverse_lazy('production_list')
        context['entity'] = 'Producción'
        return context


class ProductionCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = production
    form_class = ProductionForm
    template_name = 'production/create.html'
    success_url = reverse_lazy('production_list')
    url_redirect = success_url
    permission_required = 'add_production'

    def post(self, request, *args, **kwargs):
        try:
            data = {}
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():

                    products = json.loads(request.POST['products'])
                    shop = json.loads(request.POST['shopping'])

                    prod = production()
                    prod.user_id = request.user.id
                    if request.POST['date_process'] != '':
                        prod.date_process = request.POST['date_process']
                    prod.save()

                    # Guardamos la informacion de las compras de materia prima y otros
                    # con la orden de produccciona actual
                    for s in shop:
                        ps = ProductionShopping()
                        ps.production_id = prod.id
                        ps.shopping_cart_id = int(s['id_shopping'])
                        ps.product_id = int(s['id_product'])
                        ps.price = float(s['price'])
                        ps.cant = int(s['cant'])
                        ps.subtotal = float(s['subtotal'])
                        ps.save()
                        # if ps.shopping_cart.status:
                        # ps.shopping_cart.status = True
                        p = ps.shopping_cart.shoppingdetail_set.get(product_id=ps.product_id)
                        p.available -= ps.cant
                        p.save()

                    # Guardamos el detalle de los porductos que se van a producir
                    for i in products:
                        detail = detail_production()
                        detail.production_id = prod.id
                        detail.product_id = int(i['id'])
                        detail.cant = 0
                        detail.save()
                    data = {'id': prod.id}

            if action == 'search_shoppings':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                shop = Shopping.objects.filter(status=True)
                if len(term):
                    shop = shop.filter(Q(invoice_number__icontains=term) | Q(supplier__name__icontains=term))
                for i in shop.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSONPROCESS()
                    item['value'] = i.__str__()
                    data.append(item)

            if action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term)).filter(
                    Q(stock__gt=0) | Q(is_inventoried=False)).filter(
                    Q(category__name__exact='PF') | Q(category__name__exact='SP'))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear orden de producción'
        context['entity'] = 'Producción'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        return context


class ProductionUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = production
    form_class = ProductionForm
    template_name = 'production/create.html'
    success_url = reverse_lazy('production_list')
    url_redirect = success_url
    permission_required = 'change_production'

    def get_detail_shopping(self):
        data = []
        shop = self.get_object()
        for s in shop.productionshopping_set.all():
            item = s.toJSONPROCESS()
            data.append(item)
        return json.dumps(data)

    def get_details_product(self):
        data = []
        prod = self.get_object()
        for i in prod.detail_production_set.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_shoppings':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                shop = Shopping.objects.filter(status=False)
                if len(term):
                    shop = shop.filter(Q(invoice_number__icontains=term) | Q(supplier__name__icontains=term))
                for i in shop.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSONPROCESS()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term).filter(
                    Q(stock__gt=0) | Q(is_inventoried=False)).filter(
                    Q(category__name__exact='PF') | Q(category__name__exact='SP'))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    shop = json.loads(request.POST['shopping'])
                    shopping_delete = json.loads(request.POST['shopping_delete'])

                    prod = self.get_object()
                    prod.user_id = request.user.id
                    if request.POST['date_process'] != '':
                        prod.date_process = request.POST['date_process']
                    prod.save()

                    # Eliminamos los datos anteriormente insertados
                    # en las tablas relacionadas
                    prod.detail_production_set.all().delete()  # Eliminamos detalle de produccion
                    prod.productionshopping_set.all().delete()  # Eliminamos compras relacionadas

                    # Guardamos la informacion de las compras de materia prima y otros
                    for s in shop:
                        ps = ProductionShopping()
                        ps.production_id = prod.id
                        ps.shopping_cart_id = int(s['id_shopping'])
                        ps.product_id = int(s['id_product'])
                        ps.price = float(s['price'])
                        ps.cant = int(s['cant'])
                        ps.subtotal = float(s['subtotal'])
                        ps.save()
                        # Agregamos la disponibilidad de los elementos eliminados
                        # Aun no tomaremos en cuenta el status de la factura
                        # Se cambiara cuando no tenga ningun insumo disponible
                        # ps.shopping_cart.status = True
                        p = ps.shopping_cart.shoppingdetail_set.get(product_id=ps.product_id)
                        # Validamos si encontramos la variable a validar en el diccionario
                        # de esa manera validamos el disponible de manera correcta y solamente a los items que sufrieron
                        # cambios vamos a modificar los otros no
                        if 'before_cant' in s:
                            p.available = (p.available + int(s['before_cant'])) - ps.cant
                            p.save()
                    # Revertimos las disponibilidad de los productos comprados
                    # que se eliminaron al momento de actualizar la orden de produccion
                    for sd in shopping_delete:
                        p = ShoppingDetail.objects.get(
                            Q(shopping=sd['shopping_cart']) & Q(product_id=sd['id_product']))
                        p.available += sd['cant']
                        p.save()

                    # Guardamos el detalle de los porductos que se van a producir
                    for i in products:
                        detail = detail_production()
                        detail.production_id = prod.id
                        detail.product_id = int(i['id'])
                        detail.cant = 0
                        detail.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        context['shoppings'] = self.get_detail_shopping()
        return context
