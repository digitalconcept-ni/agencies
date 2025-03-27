import json

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from core.pos.forms import ShoppingForm, SupplierForm, ProductForm, WarehouseForm
from core.pos.mixins import ValidatePermissionRequiredMixin, ExistsCompanyMixin
from core.pos.models import Product, Shopping, Supplier, ShoppingDetail, Warehouse, ProductWarehouse
from core.reports.forms import ReportForm


class WarehouseListView(ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'warehouse/list.html'
    permission_required = 'view_warehouse'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [i.toLIST() for i in Warehouse.objects.all()]
            elif action == 'delete':
                sho = Shopping.objects.get(id=request.POST['id'])
                for s in sho.shoppingdetail_set.all():
                    s.product.stock -= s.cant
                    s.product.save()
                sho.delete()
            elif action == 'search_products_detail':
                data = []
                for i in ProductWarehouse.objects.select_related().filter(warehouse__id=request.POST['warehouse_id']):
                    data.append([i.product.__str__(), f'{i.stock:.2f}'])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listada de bodegas'
        context['create_url'] = reverse_lazy('warehouse_create')
        context['list_url'] = reverse_lazy('warehouse_list')
        context['entity'] = 'Bodegas'
        return context


class WarehouseCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse/create.html'
    success_url = reverse_lazy('warehouse_list')
    url_redirect = success_url
    permission_required = 'add_bodega'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_product_by_category':
                products = Product.objects.filter(category=request.POST['categoryID'])
                data = [i.toJSON() for i in products]
            elif action == 'search_products':
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
                products = Product.objects.filter(is_inventoried=True).filter(
                    Q(name__icontains=term) | Q(code__icontains=term))
                for i in products.filter(stock__gt=0).exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    # Json donde recolectamos los productos insertados por el usuario
                    products = json.loads(request.POST['products'])

                    # Verificamos si ya exste una bodega
                    existCentra = Warehouse.objects.filter(is_central=1).exists()

                    w = Warehouse()
                    w.code = request.POST['code']
                    w.name = request.POST['name']
                    if existCentra:
                        w.is_central = 0
                    else:
                        w.is_central = 1
                    w.description = request.POST['description']
                    w.status = request.POST['status']
                    w.save()

                    for p in products:
                        wp = ProductWarehouse()
                        wp.product_id = int(p['id'])
                        wp.warehouse_id = w.id
                        wp.stock = p['cant']
                        wp.save()

                    data = {'id': w.id}
            elif action == 'create_new_product':
                with transaction.atomic():
                    form = ProductForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'Error en el action'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear bodega'
        context['entity'] = 'Bodegas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class WarehouseUpdateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse/create.html'
    success_url = reverse_lazy('warehouse_list')
    url_redirect = success_url
    permission_required = 'change_bodega'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = WarehouseForm(instance=instance)
        # form.fields['supplier'].queryset = Supplier.objects.filter(id=instance.supplier.id)
        return form

    def get_details_product(self):
        data = []
        warehouse = self.get_object()
        for i in warehouse.productwarehouse_set.all():
            item = i.product.toJSON()
            item['cant'] = f'{i.stock:.2f}'
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
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(name__icontains=term)
                for i in products:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    # Json donde optenemos los productos insertados por el usuario
                    products = json.loads(request.POST['products'])
                    # products_delete = json.loads(request.POST['products_delete'])

                    print(products)

                    w = self.get_object()
                    w.code = request.POST['code']
                    w.name = request.POST['name']
                    w.description = request.POST['description']
                    w.status = request.POST['status']
                    w.save()

                    w.productwarehouse_set.all().delete()

                    for p in products:
                        wp = ProductWarehouse()
                        wp.product_id = int(p['id'])
                        wp.warehouse_id = w.id
                        wp.stock = float(p['cant'])
                        wp.save()

                    data = {'id': w.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de bodega'
        context['entity'] = 'Bodegas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        return context
