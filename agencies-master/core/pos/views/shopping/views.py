import json

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView
# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

from core.pos.forms import ShoppingForm, SupplierForm, ProductForm
from core.pos.mixins import ValidatePermissionRequiredMixin, ExistsCompanyMixin
from core.pos.models import Product, Shopping, Supplier, ShoppingDetail, ProductWarehouse, Warehouse
from core.reports.forms import ReportForm


class ShoppingListView(ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'shopping/list.html'
    permission_required = 'view_shopping'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Shopping.objects.select_related()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toLIST())
            elif action == 'delete':
                sho = Shopping.objects.get(id=request.POST['id'])
                warehouse_update = []
                for s in sho.shoppingdetail_set.all():
                    product_warehouse = ProductWarehouse.objects.get(
                        warehouse_id=sho.warehouse_id, product_id=s.product_id)
                    product_warehouse.stock -= s.cant
                    warehouse_update.append(product_warehouse)

                ProductWarehouse.objects.bulk_update(warehouse_update, ['stock'])
                sho.delete()
            elif action == 'search_invoice_number':
                data = []
                queryset = Shopping.objects.all()
                queryset = queryset.filter(invoice_number=request.POST['invoice'])
                data = [i.toJSON() for i in queryset]
                # data.append(queryset.toJSON())
            elif action == 'search_products_detail':
                data = []
                for i in ShoppingDetail.objects.filter(shopping_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('shopping_create')
        context['list_url'] = reverse_lazy('shopping_list')
        context['entity'] = 'Compras'
        return context


class ShoppingCreateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Shopping
    form_class = ShoppingForm
    template_name = 'shopping/create.html'
    success_url = reverse_lazy('shopping_list')
    url_redirect = success_url
    permission_required = 'add_shopping'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(Q(stock__gt=0) | Q(is_inventoried=False))
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))
                for i in products:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():

                    # Json donde recolectamos los productos insertados por el usuario
                    details = json.loads(request.POST['details'])
                    products = details['products']

                    # Diccionaro donde almacenaremos los id de los producto y sus valores
                    shopping_details = []
                    product_update = []
                    warehouse_update = []
                    cantItemsShopping = 0

                    shopping = Shopping()
                    shopping.supplier_id = int(request.POST['supplier'])
                    shopping.warehouse_id = int(request.POST['warehouse'])
                    shopping.user_id = request.user.id
                    shopping.invoice_number = request.POST['invoice_number']
                    shopping.date_joined = request.POST['date_joined']
                    shopping.discount = float(details['discount'])
                    shopping.iva = float(details['iva'])
                    shopping.income_tax = float(details['income_tax'])
                    shopping.city_tax = float(details['city_tax'])
                    shopping.save()

                    for p in products:
                        shoppingDetail = ShoppingDetail(
                            shopping_id=shopping.id,
                            product_id=int(p['id']),
                            cant=int(p['cant']),
                            available=int(p['cant']),
                            price=float(p['cost']),
                            subtotal=float(p['subtotal']),
                        )
                        # Agregamos la instancia creada para la actualizacion masiva
                        shopping_details.append(shoppingDetail)

                        # detail = ShoppingDetail()
                        # detail.shopping_id = shopping.id
                        # detail.product_id = int(i['id'])
                        # detail.cant = int(i['cant'])
                        # detail.available = int(i['cant'])
                        # detail.price = float(i['cost'])
                        # detail.subtotal = detail.cant * detail.price
                        # detail.save()

                        # Agregando datos al diccionario de productos

                        product = shoppingDetail.product
                        if not product.is_inventoried:
                            product.is_inventoried = True

                        product.cost = float(p['cost'])
                        product.pvp = float(p['pvp'])
                        product.expiration = p['expiration']

                        # Optenemos el producto y la bodega a la cual actulizaremos
                        product_warehouse = ProductWarehouse.objects.filter(
                            warehouse_id=shopping.warehouse_id, product_id=int(p['id'])).first()

                        # Si el producto en la bodega no existe, lo creamos
                        if product_warehouse is None:
                            warehouse = ProductWarehouse()
                            warehouse.warehouse_id = shopping.warehouse_id
                            warehouse.product_id = product.id
                            warehouse.stock = p['cant']
                            warehouse.save()
                        else:
                            # Sumamos la compra del producto a la bodega
                            product_warehouse.stock += p['cant']
                            warehouse_update.append(product_warehouse)

                        product_update.append(product)
                        cantItemsShopping += 1

                    # Actualizamos el stock de la bodega seleccionada
                    # product_updates = []
                    # for key, value in product_ids_dict.items():
                    #     product_warehouse = ProductWarehouse.objects.get(
                    #         warehouse_id=request.POST['warehouse'], product_id=key)
                    #     product_warehouse.stock += value
                    #     product_updates.append(product_warehouse)

                    ShoppingDetail.objects.bulk_create(shopping_details)
                    Product.objects.bulk_update(product_update, ['cost', 'pvp', 'expiration', 'is_inventoried'])
                    ProductWarehouse.objects.bulk_update(warehouse_update, ['stock'])

                    shopping.cant = + int(cantItemsShopping)
                    shopping.save()
                    shopping.calculate_invoice()
                    data = {'id': shopping.id}
            elif action == 'search_supplier':
                data = []
                term = request.POST['term']
                clients = Supplier.objects.filter(
                    Q(name__icontains=term) | Q(responsible__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_supplier':
                with transaction.atomic():
                    form = SupplierForm(request.POST)
                    data = form.save()
            elif action == 'create_new_product':
                with transaction.atomic():
                    form = ProductForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        context['frmSupplier'] = SupplierForm()
        context['frmProduct'] = ProductForm()
        return context


class ShoppingUpdateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Shopping
    form_class = ShoppingForm
    template_name = 'shopping/create.html'
    success_url = reverse_lazy('shopping_list')
    url_redirect = success_url
    permission_required = 'change_shopping'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = ShoppingForm(instance=instance)
        form.fields['supplier'].queryset = Supplier.objects.filter(id=instance.supplier.id)
        return form

    def get_details_product(self):
        data = []
        shopping = self.get_object()
        for i in shopping.shoppingdetail_set.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            item['before'] = True
            data.append(item)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(Q(stock__gt=0) | Q(is_inventoried=False))
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                # ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))
                for i in products:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    # Json donde optenemos los productos insertados por el usuario
                    products = json.loads(request.POST['products'])
                    products_delete = json.loads(request.POST['products_delete'])

                    # Unificamos ambas listas para poder hacer una sola actualizacion masiva
                    totalProducts = products + products_delete

                    shopping = self.get_object()
                    shopping.supplier_id = int(request.POST['supplier'])
                    shopping.warehouse_id = int(request.POST['warehouse'])
                    shopping.invoice_number = request.POST['invoice_number']
                    shopping.discount = float(request.POST['discount'])
                    shopping.iva = float(request.POST['iva'])
                    shopping.income_tax = float(request.POST['income_tax'])
                    shopping.city_tax = float(request.POST['city_tax'])
                    shopping.save()

                    shopping.shoppingdetail_set.all().delete()
                    cantItemsShopping = 0

                    # Crear detalles de compra en una lista
                    shopping_details = []
                    product_updates = []
                    warehouse_update = []

                    for p in totalProducts:
                        # Optenemos la bodega a la cual le actualizaremos el porducto
                        product_warehouse = ProductWarehouse.objects.filter(
                            warehouse_id=request.POST['warehouse'], product_id=int(p['id'])).first()

                        # Verificamos si la consulta realizada exite para proceder a eliminarlo
                        if product_warehouse is None:
                            continue

                        if 'delete' in p:
                            product_warehouse.stock -= detail.cant
                        else:
                            detail = ShoppingDetail(
                                shopping_id=shopping.id,
                                product_id=int(p['id']),
                                cant=int(p['cant']),
                                price=float(p['cost']),
                                subtotal=int(p['cant']) * float(p['cost'])
                            )
                            shopping_details.append(detail)

                            # En caso que el producto actual es NUEVO Solo le sumamos la cantidad actual
                            if 'before' not in p:
                                product_warehouse.stock += detail.cant

                            if 'initial_amount' in p:
                                # SI fue modificado le restamos el valor anterior y le sumamos la cantidad actual
                                product_warehouse.stock = (product_warehouse.stock - int(
                                    p['initial_amount'])) + detail.cant

                        warehouse_update.append(product_warehouse)

                        # Actualizar el producto
                        product = detail.product
                        product.cost = float(p['cost'])
                        product.pvp = float(p['pvp'])
                        product.expiration = p['expiration']

                        # Si el producto ingresado esta en estado NO inventariado
                        # Lo ponemos en True par aque pueda ser buscado al momento de facturar
                        if not detail.product.is_inventoried:
                            detail.product.is_inventoried = True

                        product_updates.append(product)
                        cantItemsShopping += 1
                    #
                    ShoppingDetail.objects.bulk_create(shopping_details)
                    Product.objects.bulk_update(product_updates, ['cost', 'pvp', 'expiration', 'is_inventoried'])
                    ProductWarehouse.objects.bulk_update(warehouse_update, ['stock'])

                    # Bloque para agregar el detalle de la compra a la tabla Shoopingdetails
                    # product_updates = [] # Lista para insertar los productos a actualizar stock
                    # for p in products:
                    #     detail = ShoppingDetail()
                    #     detail.shopping_id = shopping.id
                    #     detail.product_id = int(p['id'])
                    #     detail.cant = int(p['cant'])
                    #     detail.price = float(p['cost'])
                    #     detail.subtotal = detail.cant * detail.price
                    #     detail.save()
                    #
                    #     # Si el producto ingresado esta en estado NO inventariado
                    #     # Lo ponemos en True par aque pueda ser buscado al momento de facturar
                    #     if not detail.product.is_inventoried:
                    #         detail.product.is_inventoried = True
                    #
                    #     # Actualizamos los valores del producto
                    #     detail.product.cost = float(p['cost'])
                    #     detail.product.pvp = float(p['pvp'])
                    #     detail.product.expiration = p['expiration']
                    #     detail.product.save()
                    #
                    #     product_warehouse = ProductWarehouse.objects.get(
                    #         warehouse_id=request.POST['warehouse'], product_id=detail.product_id)
                    #
                    #     # En caso que el producto actual es NUEVO Solo le sumamos la cantidad actual
                    #     if 'before' not in p:
                    #         product_warehouse.stock += detail.cant
                    #     else:
                    #         if 'initial_amount' in p:
                    #             # SI fue modificado le restamos el valor anterior y le sumamos la cantidad actual
                    #             product_warehouse.stock = (product_warehouse.stock - int(p['initial_amount'])) + detail.cant
                    #
                    #     product_updates.append(product_warehouse)
                    #
                    #     # if detail.product.is_inventoried:
                    #     #     if p['id'] in pr:
                    #     #         indice = pr.index(p['id'])
                    #     #         detail.product.stock = (detail.product.stock - products_review[indice]['cant']) + \
                    #     #                                p['cant']
                    #     #         detail.product.cost = float(p['cost'])
                    #     #         detail.product.pvp = float(p['pvp'])
                    #     #         detail.product.expiration = p['expiration']
                    #     #         detail.product.save()
                    #     #     else:
                    #     #         detail.product.stock += p['cant']
                    #     #         detail.product.cost = float(p['cost'])
                    #     #         detail.product.pvp = float(p['pvp'])
                    #     #         detail.product.expiration = p['expiration']
                    #     #         detail.product.save()
                    #     # listProductId.append(p['id'])
                    #     cantItemsShopping += 1

                    # Ciclo para retroceder los cambios de los productos que fueron mal digitados
                    # if len(pr) != 0:
                    #     for i in pr:
                    #         print(i)
                    #         if i not in listProductId:
                    #             indice = pr.index(i)
                    #             detail.product_id = int(i)
                    #             detail.product.stock = detail.product.stock - products_review[indice]['cant']
                    #             detail.product.cost = float(products_review[indice]['cost'])
                    #             detail.product.pvp = float(products_review[indice]['pvp'])
                    #             detail.product.save()

                    # Restamos el stok de los porudctos qu ese eliminaron toalmente
                    # Del detalle de la factura
                    # if len(products_delete) > 0:
                    #     for pd in products_delete:
                    #         prod = Product.objects.get(id=pd['id'])
                    #         prod.stock -= pd['cant_store']
                    #         prod.stock_project -= pd['cant_project']
                    #         prod.save()

                    # Actualizacon de stock de la bodega seleccionada

                    # for key, value in product_ids_dict.items():
                    #     product_warehouse = ProductWarehouse.objects.get(
                    #         warehouse_id=request.POST['warehouse'], product_id=key)
                    #     product_warehouse.stock += value
                    #     product_updates.append(product_warehouse)

                    # Actializamos de manera masiva los productos
                    # ProductWarehouse.objects.bulk_update(product_updates, ['stock'])

                    shopping.cant = int(cantItemsShopping)
                    shopping.save()
                    shopping.calculate_invoice()
                    data = {'id': shopping.id}
            elif action == 'search_supplier':
                data = []
                term = request.POST['term']
                supplier = Supplier.objects.filter(
                    Q(name__icontains=term) | Q(responsible__icontains=term))[0:10]
                for i in supplier:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_supplier':
                with transaction.atomic():
                    form = SupplierForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        context['frmSupplier'] = SupplierForm()
        return context

# class SaleInvoicePdfView(LoginRequiredMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         try:
#             template = get_template('sale/invoice.html')
#             context = {
#                 'sale': Sale.objects.get(pk=self.kwargs['pk']),
#                 'icon': f'{settings.MEDIA_URL}logo.png'
#             }
#             html = template.render(context)
#             css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
#             pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
#             return HttpResponse(pdf, content_type='application/pdf')
#         except:
#             pass
#         return HttpResponseRedirect(reverse_lazy('sale_list'))
