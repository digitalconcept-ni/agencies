from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import SupplierForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Supplier


class SupplierListView(ValidatePermissionRequiredMixin, ListView):
    model = Supplier
    template_name = 'supplier/list.html'
    permission_required = 'view_supplier'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [i.toLIST() for i in Supplier.objects.select_related()]
                # data.append(i.toJSON())
            elif action == 'delete':
                sup = Supplier.objects.get(id=request.POST['id'])
                sup.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('supplier_create')
        context['list_url'] = reverse_lazy('supplier_list')
        context['entity'] = 'Proveedores'
        return context


class SupplierCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'Supplier/create.html'
    success_url = reverse_lazy('supplier_list')
    url_redirect = success_url
    permission_required = 'add_supplier'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Proveedor'
        context['entity'] = 'Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SupplierUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier/create.html'
    success_url = reverse_lazy('supplier_list')
    url_redirect = success_url
    permission_required = 'change_supplier'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
