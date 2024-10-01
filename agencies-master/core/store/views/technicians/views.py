from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Category
from core.store.forms import TechniciansForm
from core.store.models import Technicians


class TechnicansListView(ValidatePermissionRequiredMixin, ListView):
    model = Technicians
    template_name = 'technicians/list.html'
    permission_required = 'view_technicians'
    url_redirect = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [i.toLIST() for i in Technicians.objects.select_related()]
                # for i in Category.objects.all():
                #     data.append(i.toJSON())
            elif action == 'add':
                tech = Technicians()
                tech.user_id = request.user.id
                tech.name = str(request.POST['name']).upper()
                tech.position = request.POST['position']
                tech.save()
            elif action == 'delete':
                cat = Category.objects.get(id=request.POST['id'])
                cat.delete()
            else:
                data['error'] = 'Ha ocurrido un error un error con el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de técnicos'
        context['create_url'] = reverse_lazy('technicans_create')
        context['list_url'] = reverse_lazy('technicans_list')
        context['entity'] = 'Técnicos'
        context['form'] = TechniciansForm()
        return context


class TechnicansCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Technicians
    form_class = TechniciansForm
    template_name = 'technicians/create.html'
    success_url = reverse_lazy('technicans_list')
    url_redirect = success_url
    permission_required = 'add_technicians'

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
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear técnicos'
        context['entity'] = 'Técnicos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


# class CategoryUpdateView(ValidatePermissionRequiredMixin, UpdateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'category/create.html'
#     success_url = reverse_lazy('category_list')
#     url_redirect = success_url
#     permission_required = 'change_category'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'edit':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Edición una Categoria'
#         context['entity'] = 'Categorias'
#         context['list_url'] = self.success_url
#         context['action'] = 'edit'
#         return context
