from datetime import datetime

from django import forms
from django.forms import ModelForm

from core.pos.models import Shopping
from core.processes.models import production, specifications


class ProductionForm(ModelForm):
    # shopping_cart = forms.ModelChoiceField(queryset=Shopping.objects.filter(status=False),
    #                                        to_field_name='id', widget=forms.SelectMultiple(attrs={
    #         'class': 'form-control select2', 'required': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = production
        fields = '__all__'
        widgets = {
            'date_joined': forms.HiddenInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'autocomplete': 'off',
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'data-target': '#date_joined',
                'data-toggle': 'datetimepicker',
            }),
            'date_process': forms.DateInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'autocomplete': 'off',
                'class': 'form-control datetimepicker-input',
                'id': 'date_process',
                'data-target': '#date_process',
                'data-toggle': 'datetimepicker',
            }),
            # 'date_process': forms.DateTimeField(format='%Y-%m-%d %H:%M:%S', attrs={
            #     'class': 'form-control datetimepicker-input',
            #     'id': 'date_process',
            #     'value': datetime.now().strftime('%Y-%m-%d'),
            #     'data-toggle': 'datetimepicker',
            #     'data-target': '#date_process'
            # }),
            # 'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            # 'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }
        exclude = ['user']


class SpecificationsForm(ModelForm):
    class Meta:
        model = specifications
        fields = 'production', 'chemical_analysis', 'characteristics', 'health_certificate'
        widgets = {
            'health_certificate': forms.FileInput(attrs={
                'class': 'form-control',
            })
        }
