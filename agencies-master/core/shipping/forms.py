from datetime import datetime

from django import forms
from django.forms import ModelForm
from core.shipping.models import vehicles, deliveries


class VehiclesForm(ModelForm):
    class Meta:
        model = vehicles
        fields = '__all__'
        widgets = {
            'date_joined': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': 'form-control',
                'type': 'date',
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
            'shipping_date': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': 'form-control',
                'type': 'date',
            }),
            'delivery_date': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': 'form-control',
                'type': 'date',
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
