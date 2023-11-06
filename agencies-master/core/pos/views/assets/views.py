import datetime

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.pos.forms import AssetsForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Client, Assets
from core.user.models import User


class AssetsListView(ValidatePermissionRequiredMixin, ListView):
    model = Assets
    template_name = 'assets/list.html'
    permission_required = 'view_assets'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                today = datetime.datetime.today().strftime('%A')[:3].lower()
                query = Client.objects.select_related().filter(is_active=True)

                if today == 'mon':
                    data = [i.toLIST() for i in query.filter(Q(frequent=True) | Q(mon=True))]
                if today == 'tue':
                    data = [i.toLIST() for i in query.filter(Q(frequent=True) | Q(tue=True))]
                if today == 'wed':
                    data = [i.toLIST() for i in query.filter(Q(frequent=True) | Q(wed=True))]
                if today == 'thu':
                    data = [i.toLIST() for i in query.filter(Q(frequent=True) | Q(thu=True))]
                if today == 'fri':
                    data = [i.toLIST() for i in query.filter(Q(frequent=True) | Q(fri=True))]
                if today == 'sat':
                    data = [i.toLIST() for i in query.filter(Q(frequent=True) | Q(sat=True))]
                else:
                    data = [i.toLIST() for i in query.filter(frequent=True)]
            elif action == 'search_client':
                data = []
                query = Client.objects.select_related()
                term = request.POST['term']
                clients = query.filter(
                    Q(names__icontains=term) | Q(dni__icontains=term))[0:10]

                for i in clients:
                    item = i.toJSON()
                    item['text'] = f'{i.get_full_name()} - {i.dni}'
                    data.append(item)
            elif action == 'search_client_id':
                query = Assets.objects.filter(client_id=request.POST['id'])
                if query.count() != 0:
                    data = [i.toLIST() for i in query]
                else:
                    data['info'] = 'Este cliente no tiene activos comerciales ingresados'
            elif action == 'search_client_all':
                data = [i.toLIST() for i in Assets.objects.select_related()]
            elif action == 'delete':
                cli = Assets.objects.get(id=request.POST['id'])
                cli.delete()
            else:
                data['error'] = 'Ha ocurrido un error con el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Activos Comerciales'
        context['create_url'] = reverse_lazy('assets_create')
        context['list_url'] = reverse_lazy('assets_list')
        context['entity'] = 'Activos Comerciales'
        context['frmClient'] = Client.objects.select_related()
        return context


class AssetsCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Assets
    form_class = AssetsForm
    template_name = 'assets/create.html'
    success_url = reverse_lazy('assets_list_list')
    url_redirect = success_url
    permission_required = 'add_assets'

    # def get_form(self, form_class=None):
    #     id = self.request.user.id
    #     form = ClientForm(initial={'user': User.objects.get(id=id)})
    #     return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    form = self.get_form()
                    form.save()
                    data = form.save()
            else:
                data['error'] = 'Error del action'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un activo comercial'
        context['entity'] = 'Activos Comerciales'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class AssetsUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Assets
    form_class = AssetsForm
    template_name = 'assets/create.html'
    success_url = reverse_lazy('assets_list')
    url_redirect = success_url
    permission_required = 'change_assets'

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
        context['title'] = 'Edición un activo'
        context['entity'] = 'Activos Comerciales'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
