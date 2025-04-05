from datetime import datetime

from django import forms
from django.forms import ModelForm, modelformset_factory
from django_tenants.utils import get_tenant

from core.maps.models import Zone, Route, Modulo, ModuloDayVisit


class ZoneForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    class Meta:
        model = Zone
        fields = '__all__'
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        #     'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        # }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class RouteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['autofocus'] = True

    class Meta:
        model = Route
        fields = '__all__'
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        #     'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        # }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ModuloForm(ModelForm):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['code'].widget.attrs['autofocus'] = True

    class Meta:
        model = Modulo
        fields = '__all__'
        widgets = {
            'days': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        #     'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        # }

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #
    #     tenant = get_tenant(request=self.request)
    #     print(tenant)
    #     print(instance)
        # if tenant and not tenant.schema_name == 'public' and instance.archivo:
        #     month = datetime.datetime.now().strftime("%m")
        #     file = instance.FILES.get("limits")
        #     folder = os.path.join('limits', f'{tenant}', month, file.name)
        #     nombre_archivo_original = instance.archivo.name
        #     instance.archivo.name = f'{tenant.schema_name}/{nombre_archivo_original}'
        # if commit:
        #     instance.save()
        # return instance
        # data = {}
        # form = super()
        # try:
        #     if form.is_valid():
        #         if self.pk:
        #         instance = form.save()
        #         data = instance.toJSON()
        #     else:
        #         data['error'] = form.errors
        # except Exception as e:
        #     data['error'] = str(e)
        # return data


class ModuloDayVisitForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['day'].help_text = 'Dias de visita del modulo'

    class Meta:
        model = ModuloDayVisit
        fields = '__all__'
        widgets = {
            'day': forms.SelectMultiple(attrs={
                'class': 'select2 form-control',
                # 'style': 'width: 100%'
            }),
        }
        exclude = ['modulo']


ModuloDayVisitFormSet = modelformset_factory(ModuloDayVisit, form=ModuloDayVisitForm)
