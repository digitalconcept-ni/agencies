from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.pos.forms import CompanyForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Company


class CompanyUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('dashboard')
    url_redirect = success_url
    permission_required = 'change_company'


    # Utilziamos el metodo get, que al hacer la actualizacion del modelo, lo eliminamos
    def get(self, request, *args, **kwargs):
        cache.delete(f'cache_{request.tenant.id}')  # Eliminamos el espacion en cache al actualizar el modelo
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                if instance.pk is not None:
                    form = CompanyForm(request.POST, request.FILES, instance=instance)
                    # company = form.save(commit=False)
                    # company.tenant = request.tenant
                    # company.save()
                    form.save()
                else:
                    form = CompanyForm(request.POST, request.FILES)
                    company = form.save(commit=False)
                    company.tenant_id = request.tenant
                    company.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de mi compañia'
        context['entity'] = 'Compañia'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
