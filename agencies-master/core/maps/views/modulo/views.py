import datetime
import os

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from config import settings
from core.maps.forms import RouteForm, ModuloForm, ModuloDayVisitForm, ModuloDayVisitFormSet
from core.maps.models import Route, Modulo, ModuloDayVisit
from core.pos.mixins import ValidatePermissionRequiredMixin


class ModuloListView(ValidatePermissionRequiredMixin, ListView):
    model = Modulo
    template_name = 'modulo/list.html'
    permission_required = 'view_modulo'

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
        context['title'] = 'Listado de modulos'
        context['create_url'] = reverse_lazy('modulo_create')
        context['list_url'] = reverse_lazy('modulo_list')
        context['entity'] = 'Modulos'
        return context


class ModuloCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'modulo/create.html'
    success_url = reverse_lazy('modulo_list')
    url_redirect = success_url
    permission_required = 'add_modulo'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ModuloForm(request.POST, request.FILES, request=request)
                if form.is_valid():
                    form.save()
                # month = datetime.datetime.now().strftime("%m")
                # file = request.FILES.get("limits")
                # folder = os.path.join('limits', f'{request.tenant}', month, file.name)
                #
                # modulo = Modulo()
                # modulo.route_id = request.POST['route']
                # modulo.code = request.POST['code']
                # modulo.ubigeo = request.POST['ubigeo']
                # modulo.limits = file.name
                # modulo.save()
                #
                # days = ModuloDayVisit.objects.filter(day__in=request.POST['days'])
                # modulo.days.set(days)
                #
                # # Guarda el archivo usando el sistema de almacenamiento de Django
                # file_path = default_storage.save(folder, file)
            else:
                data['error'] = 'Ha ocurrido un problema con el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear modulo'
        context['entity'] = 'Modulos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # context['formSet'] = ModuloDayVisitForm()
        return context


class ModuloUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'modulo/create.html'
    success_url = reverse_lazy('modulo_list')
    url_redirect = success_url
    permission_required = 'change_modulo'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                print(request.POST)
                form = ModuloForm(request.POST, request.FILES, instance=self.object)
                if form.is_valid():
                    form.save()
                # month = datetime.datetime.now().strftime("%m")
                # file = request.FILES.get("limits")
                #
                # modulo = self.get_object()
                # modulo.route_id = request.POST['route']
                # modulo.code = request.POST['code']
                # modulo.ubigeo = request.POST['ubigeo']
                # if file is not None:
                #     folder = os.path.join('limits', f'{request.tenant}', month, file.name)
                #     modulo.limits = file.name
                #     # Guarda el archivo usando el sistema de almacenamiento de Django
                #     file_path = default_storage.save(folder, file)
                # modulo.save()
                #
                # days = ModuloDayVisit.objects.filter(day__in=request.POST['days'])
                # modulo.days.set(days)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar ruta'
        context['entity'] = 'Rutas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
