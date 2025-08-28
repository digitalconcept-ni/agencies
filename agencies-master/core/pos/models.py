from datetime import datetime

from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from client.models import Client
from config import settings
from core.pos.choices import genders, payment, municipality, tax_type, printer
from core.user.models import User


class Company(models.Model):
    tenant = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)  # new in 09-04-25
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    ruc = models.CharField(max_length=14, verbose_name='Ruc')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    mobile = models.CharField(max_length=8, verbose_name='Teléfono Celular')
    phone = models.CharField(max_length=8, verbose_name='Teléfono Convencional')
    website = models.CharField(max_length=60, verbose_name='Website')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    # printer = models.CharField(choices=printer, max_length=10, null=True, blank=True, verbose_name='Tipo de impresora')
    control_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Company'),
        )
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toLIST(self):
        data = [
            self.id, self.name, self.desc, self.id
        ]
        return data

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    phone_number = models.CharField(max_length=8, verbose_name='Numero de telefono')
    email = models.EmailField(verbose_name='Correo electronico', null=True, blank=True)
    responsible = models.CharField(max_length=30, verbose_name='Responsable', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return f'{self.name} ({self.responsible})'

    def toLIST(self):
        data = [
            self.id, self.name, self.phone_number, self.email,
            self.responsible, self.id
        ]
        return data

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']


class Brands(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.CharField(max_length=100, verbose_name='Descripcion', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_full_name(self):
        return f'{self.name}'

    def toLIST(self):
        data = [self.id, self.name, self.description, self.id]
        return data

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['-id']


# Modelo para crear bodegas
class Warehouse(models.Model):
    STATUS_CHOICE = (
        (1, 'ACTIVA'),
        (0, 'INACTIVA'),
    )

    CENTRAL_CHOICE = (
        (1, 'SI'),
        (0, 'NO'),
    )

    code = models.CharField(max_length=6, verbose_name='Codigo')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=100, verbose_name='Descripcion', null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICE, default=1, verbose_name='Estado')
    is_central = models.IntegerField(choices=CENTRAL_CHOICE, default=1, verbose_name='¿Es central?')

    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['-id']

    def __str__(self):
        return f'{self.code} | {self.name}'

    def toLIST(self):
        item = [
            self.id, self.code, self.name, self.get_is_central_display(), self.description, self.get_status_display(),
            self.id
        ]
        return item


class Product(models.Model):
    UDM_CHOICE = (
        ('und', 'UND'),
        ('lb', 'LIBRA'),
        ('kg', 'KG'),
        ('gr', 'GR'),
        ('onz', 'ONZ'),
        ('lt', 'LT'),
        ('ml', 'ML'),
        ('cuarta', 'CUARTA'),
        ('bolson', 'BOLSON'),
        ('bolsa', 'BOLSA'),
        ('caja', 'CAJA'),
        ('cajilla', 'CAJILLA'),
        ('cajon', 'CAJON'),
        ('pq', 'PAQ'),
        ('ristra', 'RISTRA'),
        ('docena', 'DOCENA'),
        ('paca', 'PACA'),
        ('qq', 'QQ'),
        ('bidon', 'BIDON'),
        ('balde', 'BALDE'),
        ('par', 'PAR'),
    )

    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name='Marca', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    code = models.CharField(max_length=13, unique=True, verbose_name='Codigo de producto')
    tax = models.CharField(max_length=7, default='exento', choices=tax_type, verbose_name='Impuesto')
    um = models.CharField(max_length=20, null=True, blank=True, verbose_name='Unidad de medida')
    udm = models.CharField(max_length=10, default='und', choices=UDM_CHOICE, verbose_name='Unidad de medida')
    expiration = models.DateField(verbose_name='Fecha de vencimiento', null=True, blank=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    is_inventoried = models.BooleanField(default=True, blank=True, null=True, verbose_name='¿Es inventariado?')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    cost = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de compra')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta #1')
    pvp2 = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta #2')
    pvp3 = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta #3')

    def __str__(self):
        # Validamos si tiene la unidad de medida anterior
        # De lo contrario optenemos la lista
        if self.um:
            udm = self.um
        else:
            udm = self.get_udm_display()

        if self.brand is None:
            brand = ' '
        else:
            brand = self.brand.name
        return f'{self.code} | {brand} {self.name} {udm}'

    def get_total_earnings(self):
        # return sum([payment.amount for payment in self.objects.all()])
        s = self.objects.all().aggregate(
            result=Sum(F('cost'), 0.00, output_field=FloatField())).get('result')
        return s

    def toLIST(self):
        if self.brand is None:
            brand = 1
        else:
            brand = self.brand.get_full_name()

        if self.expiration is None:
            ex = 'No registrada'
        else:
            ex = self.expiration.strftime('%Y-%m-%d')

        data = [
            self.id, brand, self.category.name, self.__str__(), ex, self.tax,
            self.is_inventoried, f'{self.cost:,.2f}', f'{self.pvp:,.2f}', f'{self.pvp2:,.2f}',
            f'{self.pvp3:,.2f}', self.id
        ]
        return data

    def toJSON(self):

        if self.brand is None:
            brand = 1
        else:
            brand = self.brand.toJSON()
        if self.expiration is None:
            ex = 'No registrada'
        else:
            ex = self.expiration.strftime('%Y-%m-%d')
        item = model_to_dict(self)
        if self.category:
            item['category'] = self.category.toJSON()
        item['full_name'] = self.__str__()
        item['expiration'] = ex
        item['brand'] = brand
        item['restore'] = False
        item['image'] = self.get_image()
        item['pvp'] = f'{self.pvp:.2f}'
        item['pvp2'] = f'{self.pvp2:.2f}'
        item['pvp3'] = f'{self.pvp3:.2f}'
        if item.get('cost') is not None:
            item['cost'] = f'{self.cost:.2f}'
        else:
            item['pvpc'] = f'{100.20:.2f}'
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


# Modelo que relaciona los productos con las bodehas
class ProductWarehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='Bodega')
    stock = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Stock')

    class Meta:
        verbose_name = 'Producto_Bodega'
        verbose_name_plural = 'Productos_Bodegas'
        ordering = ['id']

    def __str__(self):
        return f'{self.warehouse.name} - {self.warehouse.code}'

    def toLIST(self):
        item = [
            self.id, self.warehouse.code, self.warehouse.name, self.warehouse.description, self.id
        ]
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item['product'] = self.product.__str__()
        return item


class Shopping(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')
    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.CASCADE, verbose_name='Bodega')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    cant = models.IntegerField(default=0)
    invoice_number = models.CharField(max_length=10, default='F000000000')
    register = models.BooleanField(default=True)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    # Calculated invoice
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Subtotal')
    discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Descuento')
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='IVA')
    income_tax = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='2%')
    city_tax = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='1%')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='total')
    # Estaod para validad si la factura tiene disponibilidad de items para prroduccion
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.invoice_number} - {self.supplier.name}'

    def get_number(self):
        return f'{self.id:06d}'

    def toLIST(self):
        # Verificamos si la factura de compra tiene productos disponibles
        # para produccion
        available = self.shoppingdetail_set.all().aggregate(
            result=Coalesce(Sum(F('available')), 0.00, output_field=FloatField())).get('result')
        if available <= 0:
            self.status = False
            self.save()

        # Verificamos si las la fecha de registro es menos a hoy
        if self.date_joined.strftime("%Y-%m-%d") < str(datetime.now().date()):
            modify = True
        else:
            modify = False

        # Variable de opciones adicionales
        opt = [modify, self.status]

        date_joined = f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        user = f'{self.user.username} {self.time_joined.strftime("%I:%M:%S %p")}'

        data = [
            self.get_number(), user, self.warehouse.__str__(), self.supplier.name, self.invoice_number,
            date_joined, self.cant, f'{self.discount:,.2f}', f'{self.subtotal:,.2f}',
            f'{self.iva:,.2f}', f'{self.income_tax:,.2f}', f'{self.city_tax:,.2f}', f'{self.total:,.2f}',
            opt
        ]
        # data = [
        #     self.get_number(), self.user.username, self.supplier.name, self.invoice_number,
        #     self.cant, date_joined, f'{self.subtotal:,.2f}', f'{self.total_iva:,.2f}', f'{self.total:,.2f}',
        #     opt
        # ]
        return data

    def toJSONPROCESS(self):
        item = model_to_dict(self)
        item['username'] = self.user.username
        item['shopping_details'] = [i.toJSON() for i in self.shoppingdetail_set.all()]
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item['modify'] = False
        if self.date_joined.strftime("%Y-%m-%d") < str(datetime.now().date()):
            item['modify'] = True
        item['number'] = self.get_number()
        item['username'] = self.user.username
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['date_joined'] = f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        item['shopping_details'] = [i.toJSON() for i in self.shoppingdetail_set.all()]
        return item

    def calculate_invoice(self):
        subtotal = self.shoppingdetail_set.all().aggregate(
            result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal - float(self.discount)
        self.total = float(self.subtotal) + float(self.iva) + float(self.income_tax) + float(self.city_tax)
        self.save()

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-date_joined']


class ShoppingDetail(models.Model):
    shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    # Este campo lo utilizaremos para saber cuanto hay disponible
    # para las proximas producciones
    available = models.IntegerField(default=0, verbose_name='Disponible')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self)
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:,.2f}'
        item['subtotal'] = f'{self.subtotal:,.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=14, unique=True, default='0010101010034S', verbose_name='RUC')
    phone_number = models.CharField(max_length=8, default=87878787, verbose_name='Numero de telefono')
    birthdate = models.DateField(default=datetime.now, null=True, blank=True, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=genders, default='male', verbose_name='Genero')
    municipality = models.CharField(max_length=13, choices=municipality, default='managua', verbose_name='Municipio')
    frequent = models.BooleanField(verbose_name='Frecuente', default=True, null=True, blank=True)
    mon = models.BooleanField(verbose_name='Lunes', null=True, blank=True)
    tue = models.BooleanField(verbose_name='Martes', null=True, blank=True)
    wed = models.BooleanField(verbose_name='Miercoles', null=True, blank=True)
    thu = models.BooleanField(verbose_name='Jueves', null=True, blank=True)
    fri = models.BooleanField(verbose_name='Viernes', null=True, blank=True)
    sat = models.BooleanField(verbose_name='Sabados', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='activo', default=True)
    lat = models.CharField(max_length=20, null=True, blank=True, verbose_name='Latitud')
    lng = models.CharField(max_length=20, null=True, blank=True, verbose_name='Longitud')

    def __str__(self):
        return self.get_full_name()

    def get_number(self):
        return f'{self.id:06d}'

    def get_full_name(self):
        return f'{self.names}'

    def toLIST(self):
        item = model_to_dict(self)
        visit = {'frequent': 'Frecuente', 'mon': 'Lunes',
                 'tue': 'Martes', 'wed': 'Miercoles', 'thu': 'Jueves', 'fri': 'Viernes', 'sat': 'Sabados'}
        frequent = []
        for v in visit:
            if item[v]:
                frequent.append(visit[v])

        if self.birthdate:
            birthdate = self.birthdate.strftime('%Y-%m-%d')
        else:
            birthdate = ' '
        data = [self.get_number(), self.is_active, self.user.username, self.names, self.dni,
                birthdate,
                self.get_gender_display(), self.address, frequent, self.id
                ]
        return data

    def toJSON(self):
        visit = {'frequent': 'Frecuente', 'mon': 'Lunes',
                 'tue': 'Martes', 'wed': 'Miercoles', 'thu': 'Jueves', 'fri': 'Viernes', 'sat': 'Sabados'}
        frequent = []
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        print(self.birthdate)
        if self.birthdate:
            item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        else:
            item['birthdate'] = ' '
        for v in visit:
            if item[v]:
                frequent.append(visit[v])
        item['visit'] = frequent
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Assets(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    asset = models.CharField(max_length=50, verbose_name='Activo')
    code = models.CharField(max_length=20, verbose_name='Codigo')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de entrega')
    cant = models.CharField(max_length=5, verbose_name='Cantidad')
    brand = models.CharField(max_length=20, verbose_name='Marca', null=True, blank=True)
    serie = models.CharField(max_length=20, verbose_name='Número de serie', null=True, blank=True)

    def __str__(self):
        return f'{self.client.names} - {self.asset}'

    def toLIST(self):
        data = [
            self.id, self.client.names, self.asset, self.cant, self.date_joined.strftime("%Y-%m-%d"),
            self.brand, self.code, self.serie, self.id
        ]
        return data

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Activos'
        verbose_name_plural = 'Activos'
        ordering = ['-date_joined']


class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    user_commissions = models.CharField(max_length=20, null=True, blank=True, verbose_name='Usuario a comisionar')
    endofday = models.BooleanField(default=False)
    applied = models.BooleanField(default=False)
    purchase_order = models.CharField(max_length=15, blank=True, null=True, verbose_name='Orden de Compra')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    payment = models.CharField(max_length=14, choices=payment, default='cash', verbose_name='Metodo de pago')
    days = models.CharField(max_length=2, null=True, blank=True, verbose_name='Dias de gracia')
    end = models.DateField(null=True, blank=True, verbose_name='Fecha cancelacion')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal_exempt = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    # iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.client.names

    def end_day(self, session):
        if not session:
            if self.user.is_active:
                self.user.is_active = False
                self.user.save()
        self.endofday = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def get_number(self):
        return f'{self.id:06d}'

    def toLIST(self):
        modify = False
        if self.date_joined.strftime("%Y-%m-%d") < str(datetime.now().date()):
            modify = True
        opt = [modify, self.endofday, self.applied]
        data = [
            self.get_number(), self.client.get_full_name(), self.payment, self.purchase_order, self.user.username,
            self.user_commissions,
            f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}',
            f'{self.subtotal_exempt:.2f}', f'{self.subtotal:.2f}', f'{self.discount:.2f}',
            f'{self.total_iva:.2f}', f'{self.total:.2f}',
            opt
        ]
        return data

    def toJSON(self):
        item = model_to_dict(self)
        item['modify'] = False
        if self.date_joined.strftime("%Y-%m-%d") < str(datetime.now().date()):
            item['modify'] = True
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['user'] = self.user.username
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['discount'] = f'{self.discount:.2f}'
        # item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['date_joined'] = f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.filter(product__is_inventoried=True):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().filter(restore=False).filter(product__tax='grabado').aggregate(
            result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        self.total_iva = (self.subtotal - self.discount) * 0.15
        self.total = ((float(self.subtotal) + float(self.subtotal_exempt)) - float(self.discount)) + float(
            self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-id']


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    applied_price = models.CharField(max_length=4, null=True)# Precio aplicado
    cant = models.IntegerField(default=0)
    # Con este campo vamos a validar que productos de la factura los devolucionaron
    restore = models.BooleanField(default=False, verbose_name='Devolucion')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['restore'] = self.restore
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['id']


# Modelo para control de perdidas de productos

class loss(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def get_number(self):
        return f'{self.id:06d}'

    def toLIST(self):
        data = [self.get_number(), self.user.username, f'{self.date_joined.strftime("%Y-%m-%d")}',
                f'{self.time_joined.strftime("%I:%M:%S %p")}', self.total, self.id]
        return data

    class Meta:
        verbose_name = 'Perdida'
        verbose_name_plural = 'Perdidas'
        ordering = ['date_joined']


class loss_details(models.Model):
    order_loss = models.ForeignKey(loss, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    reason_loss = models.CharField(max_length=80)

    def toJSON(self):
        item = model_to_dict(self, exclude=['order_loss'])
        item['product'] = self.product.name
        return item

    class Meta:
        verbose_name = 'detalle perdida'
        verbose_name_plural = 'detalle perdidas'
        default_permissions = ()
        ordering = ['id']
