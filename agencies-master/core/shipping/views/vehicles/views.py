from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.shipping.forms import VehiclesForm
from core.shipping.models import vehicles

entity = 'vehículos'


class VehiclesListView(ValidatePermissionRequiredMixin, ListView):
    model = vehicles
    template_name = 'vehicles/list.html'
    permission_required = 'view_vehicles'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in vehicles.objects.select_related():
                    data.append(i.toLIST())
            elif action == 'delete':
                pro = vehicles.objects.get(id=request.POST['id'])
                pro.delete()
            else:
                data['error'] = 'Ha ocurrido un error revise sus valores'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de vehículos'
        context['create_url'] = reverse_lazy('vehicles_add')
        context['list_url'] = reverse_lazy('vehicles_list')
        context['entity'] = entity
        return context


class VehiclesCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = vehicles
    form_class = VehiclesForm
    template_name = 'vehicles/create.html'
    success_url = reverse_lazy('vehicles_list')
    url_redirect = success_url
    permission_required = 'add_vehicles'

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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un vehículo'
        context['entity'] = entity
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class VehiclesUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = vehicles
    form_class = VehiclesForm
    template_name = 'vehicles/create.html'
    success_url = reverse_lazy('vehicles_list')
    url_redirect = success_url
    permission_required = 'change_vehicles'

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
        context['title'] = 'Edición de un vehículo'
        context['entity'] = 'vehículos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
