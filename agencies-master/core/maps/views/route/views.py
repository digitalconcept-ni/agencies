from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.maps.forms import ZoneForm, RouteForm
from core.maps.models import Zone, Route
from core.pos.mixins import ValidatePermissionRequiredMixin


class RouteListView(ValidatePermissionRequiredMixin, ListView):
    model = Route
    template_name = 'route/list.html'
    permission_required = 'view_route'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [i.toLIST() for i in self.model.objects.select_related()]
            elif action == 'delete':
                pro = self.model.objects.get(id=request.POST['id'])
                pro.delete()
            else:
                data['error'] = 'Ha ocurrido un error revise sus valores'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de rutas'
        context['create_url'] = reverse_lazy('route_create')
        context['list_url'] = reverse_lazy('route_list')
        context['entity'] = 'Rutas'
        return context


class RouteCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'zone/create.html'
    success_url = reverse_lazy('route_list')
    url_redirect = success_url
    permission_required = 'add_route'

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
        context['title'] = 'Crear ruta'
        context['entity'] = 'Rutas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
#
#
class RouteUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'route/create.html'
    success_url = reverse_lazy('route_list')
    url_redirect = success_url
    permission_required = 'change_route'

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
        context['title'] = 'Editar ruta'
        context['entity'] = 'Rutas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context