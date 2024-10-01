from django.forms import ModelForm
from django import forms

from core.store.models import Technicians, Exits


class TechniciansForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Technicians
        fields = 'name', 'position'
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


class ExitsForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Exits
        fields = 'client', 'technician',
        widgets = {
            'client': forms.Select(attrs={
                'class': 'custom-select select2',
            }), 'technician': forms.Select(attrs={
                'class': 'custom-select select2',
            }),
        }

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data
