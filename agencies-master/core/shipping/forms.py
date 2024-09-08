from datetime import datetime

from django import forms
from django.forms import ModelForm
from core.shipping.models import vehicles, deliveries


class VehiclesForm(ModelForm):
    class Meta:
        model = vehicles
        fields = '__all__'
        widgets = {
            'date_joined': forms.HiddenInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class DeliveriesForm(ModelForm):
    class Meta:
        model = deliveries
        fields = 'sale',  'shipping_date', 'delivery_date', 'vehicle','amount', 'initial_km', 'final_km',
        widgets = {
            'date_joined': forms.HiddenInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
            }),
            'shipping_date': forms.DateInput(attrs={
                'class': 'datetimepicker-input',
                'id': 'shipping_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': 'shipping_date',
                'maxlength': '10',

            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'datetimepicker-input',
                'id': 'delivery_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': 'delivery_date',
                'maxlength': '10',
            }),
        }
        exclude = ['status', 'total_distance']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
