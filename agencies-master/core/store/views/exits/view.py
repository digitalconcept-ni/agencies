import json
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Product
from core.store.forms import ExitsForm
from core.store.models import Exits, ExitsDetail, Technicians


class ExitsListView(ValidatePermissionRequiredMixin, ListView):
    model = Exits
    template_name = 'exits/list.html'
    permission_required = 'view_technicians'
    url_redirect = reverse_lazy('dashboard')

    # Funcion que nos ayuda a saber cuantas ordenes estan completas y cuantas no
    def getCompleteOrder(self):
        data = {}
        ban = 0
        check = 0
        for e in Exits.objects.all():
            status = all(getattr(c, 'restore') for c in e.exitsdetail_set.all())
            if status:
                check += 1
            elif not status:
                ban += 1

        data['check'] = check
        data['ban'] = ban

        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            action = request.POST['action']
            if action == 'search_technician_select2':
                data = []
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                tech = Technicians.objects.filter(Q(name__icontains=term) | Q(position__icontains=term))
                for i in tech:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            if action == 'search_products_select2':
                data = []
                # ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))
                for i in products:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            if action == 'search_data':
                # Busqueda global de todos los porductos
                today = datetime.now().date()
                data = [i.toLIST() for i in Exits.objects.select_related().filter(date_joined=today)]

            if action == 'search_product_detail':
                # Busqueda de todas las salidas en las cuales este el producto seleccionado
                ed = ExitsDetail.objects.filter(product_id=request.POST['id']).values_list('exit', flat=True)
                data = [i.toLIST() for i in Exits.objects.filter(id__in=ed)]

            if action == 'search_technician_detail':
                # Busqueda de orden segun el tecnico seleccionado
                data = [i.toLIST() for i in Exits.objects.filter(technician_id=request.POST['id'])]
                print(data)

            if action == 'search_exit_detail':
                # data = [ed.toLIST() for ed in ExitsDetail.objects.filter(exit_id=request.POST['id'])]
                # item = 0
                for ed in ExitsDetail.objects.filter(exit_id=request.POST['id']):
                    data.append(ed.toJSON())

            if action == 'delete':
                e = Exits.objects.get(id=request.POST['id'])
                set = e.exitsdetail_set.all()
                for s in set:
                    s.product.stock += s.cant
                    s.product.save()
                e.delete()

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de salidas'
        context['create_url'] = reverse_lazy('exits_create')
        context['entity'] = 'Salidas'
        context['list_url'] = reverse_lazy('exits_list')
        context['verify'] = self.getCompleteOrder()
        return context


class ExitsCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Exits
    form_class = ExitsForm
    template_name = 'exits/create.html'
    success_url = reverse_lazy('exits_list')
    url_redirect = success_url
    permission_required = 'add_create'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term)).filter(
                    Q(stock__gt=0) | Q(is_inventoried=False))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])

                    exit = Exits()
                    exit.technician_id = request.POST['technician']
                    exit.client_id = request.POST['client']
                    exit.user_id = int(request.user.id)
                    exit.save()

                    for p in products:
                        ed = ExitsDetail()
                        ed.exit_id = exit.id
                        ed.product_id = p['product_id']
                        ed.cant = p['cant']
                        ed.restore = bool(p['restore'])
                        ed.save()
                        if str(p['category']).upper() == 'MATERIA PRIMA' or str(p['category']).upper() == 'INSUMOS':
                            print(p['category'])
                            ed.product.stock -= p['cant']
                            ed.save()

                    # Validamos si todos los porductos han sido devueltos
                    # Si fueronn devuletos el estados de la salida es completa
                    exit.status = all(getattr(c, 'restore') for c in exit.exitsdetail_set.all())
                    exit.save()
            else:
                data['error'] = 'Error en el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de salida'
        context['entity'] = 'Salidas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ExitsUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Exits
    form_class = ExitsForm
    template_name = 'exits/create.html'
    success_url = reverse_lazy('exits_list')
    url_redirect = success_url
    permission_required = 'add_update'

    def get_detail_exit(self):
        data = []
        ed = self.get_object()
        for s in ed.exitsdetail_set.all():
            item = s.toJSON()
            data.append(item)
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
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term)).filter(
                    Q(stock__gt=0) | Q(is_inventoried=False))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    # products_delete = json.loads(request.POST['products_delete'])

                    exit = self.get_object()
                    exit.technician_id = request.POST['technician']
                    exit.client_id = request.POST['client']
                    exit.user_id = int(request.user.id)
                    exit.save()

                    # Eliminamo sel registro de los productos prestados
                    exit.exitsdetail_set.all().delete()

                    # Insertamos los productos que se agregaron al detalle
                    for p in products:
                        ed = ExitsDetail()
                        ed.exit_id = exit.id
                        ed.product_id = p['product_id']
                        ed.cant = p['cant']
                        ed.restore = bool(p['restore'])
                        ed.save()
                        if 'before_cant' in p:
                            print(p['before_cant'])
                            if str(p['category']).upper() == 'MATERIA PRIMA' or str(p['category']).upper() == 'INSUMOS':
                                ed.product.stock = (ed.product.stock + int(p['before_cant'])) - p['cant']
                                ed.product.save()

                    # Validamos si todos los porductos han sido devueltos
                    # Si fueronn devuletos el estados de la salida es completa
                    exit.status = all(getattr(c, 'restore') for c in exit.exitsdetail_set.all())
                    exit.save()

            else:
                data['error'] = 'No ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificación de salida'
        context['entity'] = 'Salidas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['detail'] = self.get_detail_exit()
        return context

# class BoxesDeleteView(LoginRequiredMixin, DeleteView):
#     model = Boxes
#     form_class = BoxesForms
#     template_name = 'boxes/delete.html'
#     success_url = reverse_lazy('inventory:listados_list')
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             self.object.delete()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Eliminar Caja'
#         context['entity'] = 'Cajas'
#         context['list_url'] = self.success_url
#         context['action'] = 'delete'
#         return context
