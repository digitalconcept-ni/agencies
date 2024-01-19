from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.pos.forms import BrandsForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Brands


class BrandListView(ValidatePermissionRequiredMixin, ListView):
    model = Brands
    template_name = 'brands/list.html'
    permission_required = 'view_brands'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Brands.objects.select_related():
                    data.append(i.toLIST())
            elif action == 'delete':
                pro = Brands.objects.get(id=request.POST['id'])
                pro.delete()
            else:
                data['error'] = 'Ha ocurrido un error en el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Marcas'
        context['create_url'] = reverse_lazy('brand_create')
        context['list_url'] = reverse_lazy('product_list')
        context['entity'] = 'Marcas'
        return context


class BrandsCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Brands
    form_class = BrandsForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('brand_list')
    url_redirect = success_url
    permission_required = 'add_brands'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'Error en el action, revisarlo.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una marca'
        context['entity'] = 'Marcas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class BrandsUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Brands
    form_class = BrandsForm
    template_name = 'brands/create.html'
    success_url = reverse_lazy('brand_list')
    url_redirect = success_url
    permission_required = 'change_brands'

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
                data['error'] = 'Ocurrio un error en el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una marca'
        context['entity'] = 'Marcas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context