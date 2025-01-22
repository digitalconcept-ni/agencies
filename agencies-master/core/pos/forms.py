from django import forms
from django.forms import ModelForm
from core.pos.models import *


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }

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


class BrandsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Brands
        fields = '__all__'
        # widgets = {
        #     'expiration': forms.DateInput(format='%Y-%m-%d', attrs={
        #         'class': 'form-control datetimepicker-input',
        #         'id': 'expiration',
        #         'value': datetime.now().strftime('%Y-%m-%d'),
        #         'data-toggle': 'datetimepicker',
        #         'data-target': '#birthdate'
        #     }),
        #     'category': forms.Select(attrs={
        #             'class': 'select2',
        #             'style': 'width: 100%'
        #         }),
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


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'expiration': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'type': 'date',
            }),
            'category': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
        }

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


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        # self.fields['user'].queryset = User.objects.filter(id=self.request.user.id)

    class Meta:
        model = Client
        fields = 'user', 'names', 'dni', 'birthdate', 'address', 'municipality', 'gender', 'lat', 'lng', 'is_active', 'frequent', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'
        widgets = {
            # 'user': forms.Select(attrs={
            #     'class': 'custom-select select2',
            #     # 'style': 'width: 100%'
            # }),
            'user': forms.Select(),
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese un número de cedula'}),
            'birthdate': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'type': 'date',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Ingrese una dirección',
            }),
            'gender': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
            'frequent': forms.CheckboxInput(),
            'mon': forms.CheckboxInput(),
            'tue': forms.CheckboxInput(),
            'wed': forms.CheckboxInput(),
            'thu': forms.CheckboxInput(),
            'fri': forms.CheckboxInput(),
            'sat': forms.CheckboxInput(),
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


class AssetsForm(ModelForm):
    class Meta:
        model = Assets
        fields = '__all__'
        widgets = {
            'date_joined': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
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


class SupplierForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Supplier
        fields = '__all__'
        # widgets = {
        #     'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        #     'dni': forms.TextInput(attrs={'placeholder': 'Ingrese un número de cedula'}),
        #     'birthdate': forms.DateInput(format='%Y-%m-%d', attrs={
        #         'class': 'form-control datetimepicker-input',
        #         'id': 'birthdate',
        #         'value': datetime.now().strftime('%Y-%m-%d'),
        #         'data-toggle': 'datetimepicker',
        #         'data-target': '#birthdate'
        #     }),
        #     'address': forms.TextInput(attrs={
        #         'placeholder': 'Ingrese una dirección',
        #     }),
        #     'gender': forms.Select(attrs={
        #         'class': 'select2',
        #         'style': 'width: 100%'
        #     })
        # }

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


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.none()
        self.fields['user_com'].required = False

    user_com = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name='username', widget=forms.Select(attrs={
        'class': 'form-control select2'}))

    # user_com = forms.Select()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {

            'end': forms.DateInput(attrs={
                'readonly': True,
                'value': datetime.now().strftime('%Y-%m-%d'),
            }),
            'user_commissions': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'purchase_order': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'client': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.HiddenInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'autocomplete': 'off',
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'data-target': '#date_joined',
                'data-toggle': 'datetimepicker',
            }),
            # 'iva': forms.TextInput(attrs={
            #     'class': 'form-control',
            # }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'subtotal_exempt': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'discount': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }


class SaleMovilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # print(self.user)
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.none()
        self.fields['user_com'].required = False

    user_com = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name='username', widget=forms.Select(attrs={
        'class': 'form-control select2', 'required': False}))

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'user_commissions': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'client': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.HiddenInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'autocomplete': 'off',
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'data-target': '#date_joined',
                'data-toggle': 'datetimepicker',
            }
            ),
            'end': forms.DateInput(attrs={
                'readonly': True,
                'value': datetime.now().strftime('%Y-%m-%d'),
            }),
            # 'iva': forms.TextInput(attrs={
            #     'style': 'border: none; width: 100%; background: transparent; color: white;'
            # }),
            'subtotal_exempt': forms.TextInput(attrs={
                'readonly': True,
                'style': 'border: none; width: 100%; background: transparent; color: white;',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'style': 'border: none; width: 100%; background: transparent; color: white;'
            }),
            'discount': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'style': 'border: none; width: 100%; background: transparent; color: white;'
            })
        }


class ShoppingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.none()

    class Meta:
        model = Shopping
        fields = '__all__'
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.TextInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': 'form-control',
                'type': 'date',
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': False
            }),
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'printer': forms.Select(attrs={'class': 'custom-select select2', }),
        }

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


class LossForm(ModelForm):
    class Meta:
        model = loss
        fields = '__all__'
        widgets = {
            'date_joined': forms.HiddenInput(attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
            }),
        }
