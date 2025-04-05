from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.maps.forms import ZoneForm
from core.maps.models import Zone
from core.pos.mixins import ValidatePermissionRequiredMixin


class ZoneListView(ValidatePermissionRequiredMixin, ListView):
    model = Zone
    template_name = 'zone/list.html'
    permission_required = 'view_zone'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [i.toLIST() for i in Zone.objects.select_related()]
            elif action == 'delete':
                pro = Zone.objects.get(id=request.POST['id'])
                pro.delete()
            else:
                data['error'] = 'Ha ocurrido un error revise sus valores'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de zonas'
        context['create_url'] = reverse_lazy('zone_create')
        context['list_url'] = reverse_lazy('zone_list')
        context['entity'] = 'Zonas'
        return context


class ZoneCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/create.html'
    success_url = reverse_lazy('zone_list')
    url_redirect = success_url
    permission_required = 'add_zone'

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
        context['title'] = 'Crear zona'
        context['entity'] = 'Zonas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
#
#
class ZoneUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/create.html'
    success_url = reverse_lazy('zone_list')
    url_redirect = success_url
    permission_required = 'change_zone'

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
        context['title'] = 'Editar zona'
        context['entity'] = 'Zonas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context