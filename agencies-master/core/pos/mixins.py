from datetime import datetime

from crum import get_current_request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from core.pos.forms import SaleMovilForm, SaleForm
from core.pos.models import Company, Client


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('dashboard')
        return self.url_redirect

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request = get_current_request()
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            return super().get(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())


class ExistsCompanyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if Company.objects.all().exists():
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No se puede facturar si no esta registrada la compañia')
        return redirect('dashboard')


class deviceVerificationMixin(object):

    # def get_form(self, form_class=None):
    #     module = self.request.path.split('/')[3]
    #     print(module)
    #     if module == 'update':
    #         instance = self.get_object()
    #         if 'Sec-Ch-Ua-Mobile' in self.request.headers:
    #             if self.request.headers['Sec-Ch-Ua-Mobile'] == '?1':
    #                 form = SaleMovilForm(instance=instance)
    #                 form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
    #             elif self.request.headers['Sec-Ch-Ua-Mobile'] == '?0':
    #                 form = SaleForm(instance=instance)
    #                 form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
    #             return form

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if 'Sec-Ch-Ua-Mobile' in request.headers:
            if request.headers['Sec-Ch-Ua-Mobile'] == '?1':
                self.form_class = SaleMovilForm
                self.template_name = 'sale/createmovil2.html'
            elif request.headers['Sec-Ch-Ua-Mobile'] == '?0':
                self.form_class = SaleForm
                self.template_name = 'sale/create.html'
        else:
            self.form_class = SaleForm
            self.template_name = 'sale/create.html'
        return super().dispatch(request, *args, **kwargs)
