from datetime import datetime

import json
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, CreateView, UpdateView

from core.pos.mixins import ExistsCompanyMixin, ValidatePermissionRequiredMixin
from core.pos.models import Product, Shopping
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
        print(valores_por_clave)

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
                # Separamos la fecha inicial y la fecha final
                sds = start_date.split('-')
                eds = end_date.split('-')
                # Creamos la fecha con hora para no tener inconvenientes en la busqueda de las ordenes
                sd = datetime(int(sds[0]), int(sds[1]), int(sds[2]), 00, 00, 00)
                ed = datetime(int(eds[0]), int(eds[1]), int(eds[2]), 23, 59, 00)
                if len(start_date) and len(end_date) and request.user.is_superuser:
                    queryset = queryset.filter(date_joined__range=[sd, ed])
                elif len(start_date) and len(end_date) and not request.user.is_superuser:
                    queryset = queryset.filter(
                        Q(user_id=request.user.id) & Q(date_joined__range=[sd, ed]))
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

                print(calc)

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
                p = production.objects.get(id=request.POST['id']).productionshopping_set.all()
                shopping = []
                total = 0.00

                for ps in p:
                    total += float(ps.shopping_cart.total)
                    shopping.append({'id': ps.id, 'invoice': ps.shopping_cart.invoice_number,
                                     'supplier': ps.shopping_cart.supplier.name, 'total': ps.shopping_cart.total})
                shopping.append(
                    {'id': '---------', 'invoice': '---------', 'supplier': '---------', 'total': total})

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

                    prod = production()
                    prod.user_id = request.user.id
                    prod.date_joined = request.POST['date_joined']
                    if request.POST['date_process'] != '':
                        prod.date_process = request.POST['date_process']
                    prod.save()

                    # Recolectamos los id de las compras para poder saar los costoss de cada saco producido
                    idShopping = request.POST.getlist('shopping_cart')
                    psList = []

                    # Guardamos las facturas relacionadas para la produccion creada

                    for s in idShopping:
                        changeStatus = Shopping.objects.get(id=s)
                        changeStatus.status = True
                        changeStatus.save()
                        ps = ProductionShopping(
                            production_id=prod.id,
                            shopping_cart_id=int(s)
                        )
                        psList.append(ps)
                    # Guardamos de manera masiva los id relacionados de la produccion con las compras
                    ProductionShopping.objects.bulk_create(psList)

                    for i in products:
                        detail = detail_production()
                        detail.production_id = prod.id
                        detail.product_id = int(i['id'])
                        detail.cant = 0
                        detail.save()
                    data = {'id': prod.id}

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
        id = self.request.user.id
        # form = ClientForm(initial={'user': User.objects.get(id=id)})
        # form.fields['user'].widget.attrs['hidden'] = True
        # context['frmClient'] = form
        return context


class ProductionUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = production
    form_class = ProductionForm
    template_name = 'production/create.html'
    success_url = reverse_lazy('production_list')
    url_redirect = success_url
    permission_required = 'change_production'

    def get_details_product(self):
        data = []
        prod = self.get_object()
        for i in prod.detail_production_set.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        print(data)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products_select2':
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
                    # now = datetime.now()
                    # today = str(now.date())

                    prod = self.get_object()
                    prod.user_id = request.user.id
                    prod.shopping_cart_id = request.POST['shopping_cart']
                    prod.date_joined = request.POST['date_joined']
                    if request.POST['date_process'] != '':
                        prod.date_process = request.POST['date_process']
                    prod.save()

                    # Recolectamos los id de las compras para cambiar el status
                    idShopping = request.POST.getlist('shopping_cart')
                    psList = []

                    psSet = prod.productionshopping_set.all()

                    # Le quitamos el status a las facturas ingresadas para luego aliminarlas

                    for s in psSet:
                        s.shopping_cart.status = False
                        s.save()

                    psSet.delete()

                    # Guardamos las facturas relacionadas para la produccion creada

                    for s in idShopping:
                        ps = ProductionShopping(
                            production_id=prod.id,
                            shopping_cart_id=int(s)
                        )
                        ps.shopping_cart.status = True
                        ps.save()
                        psList.append(ps)

                    prod.detail_production_set.all().delete()

                    for p in products:
                        detail = detail_production()
                        detail.production_id = prod.id
                        detail.product_id = int(p['id'])
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
        return context
