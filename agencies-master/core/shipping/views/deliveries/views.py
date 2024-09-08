from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.shipping.forms import  DeliveriesForm
from core.shipping.models import deliveries

entity = 'Delivery'


class DeliveriesListView(ValidatePermissionRequiredMixin, ListView):
    model = deliveries
    template_name = 'deliveries/list.html'
    permission_required = 'view_deliveries'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in deliveries.objects.select_related():
                    data.append(i.toLIST())
            elif action == 'delete':
                pro = deliveries.objects.get(id=request.POST['id'])
                pro.delete()
            else:
                data['error'] = 'Ha ocurrido un error revise sus valores'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de entregas'
        context['create_url'] = reverse_lazy('deliveries_add')
        context['list_url'] = reverse_lazy('deliveries_list')
        context['entity'] = entity
        return context


class DeliveriesCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = deliveries
    form_class = DeliveriesForm
    template_name = 'deliveries/create.html'
    success_url = reverse_lazy('deliveries_list')
    url_redirect = success_url
    permission_required = 'add_deliveries'

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
                data['error'] = 'Ha ocurrido un problema con el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una entrega'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class DeliveriesUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = deliveries
    form_class = DeliveriesForm
    template_name = 'deliveries/create.html'
    success_url = reverse_lazy('deliveries_list')
    url_redirect = success_url
    permission_required = 'change_deliveries'

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una entrega'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context