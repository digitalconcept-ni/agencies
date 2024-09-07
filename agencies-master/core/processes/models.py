from datetime import datetime

from django.db import models
from django.db.models import Count, Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.models import Shopping, Product
from core.user.models import User

type_product = (
    ('sp', 'Sub producto'),
    ('pf', 'Producto Final'),
)


# Create your models here.

class production(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    # shopping_cart = models.ForeignKey(Shopping, on_delete=models.CASCADE,
    #                                   null=True, blank=True, verbose_name='Materia prima')
    # lot = models.CharField(max_length=10,verbose_name='Nro Lote',)
    # False = PROCESO, True = Completo
    status = models.BooleanField(default=False, verbose_name='Estado')
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    date_process = models.DateField(null=True, blank=True, verbose_name='Fecha de proceso')
    date_end_process = models.DateField(null=True, blank=True, verbose_name='Fecha fin proceso')
    efficiency = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Eficiencia')

    def __str__(self):
        return f'{self.id} - {self.date_joined.strftime("%Y-%m-%d")}'

    # def delete(self, using=None, keep_parents=False):
    #     detail = self.productionshopping_set.all()
    #     for d in detail:
    #         d.shopping_cart.shoppingdetail_set.all().
    #         d.product.stock += detail.cant
    #         d.product.save()
    #     super(production, self).delete()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toLIST(self):
        # if self.productionshopping_set.all():
        #     shopping = []
        #     for ps in self.productionshopping_set.all():
        #         shopping.append(f'{ps.shopping_cart.invoice_number} - {ps.shopping_cart.supplier.name}')
        # else:
        #     shopping = 'No hay materia prima relacionada'

        if self.date_end_process is None:
            date_end_process = 'Sin finalizar'
        else:
            date_end_process = self.date_end_process.strftime("%Y-%m-%d ")

        if self.date_process is None or self.date_process == '':
            date_process = 'Sin comezar'
        else:
            date_process = self.date_process.strftime("%Y-%m-%d ")

        # shopping = f'{self.shopping_cart.invoice_number} - {self.shopping_cart.supplier.name}'
        date_joined = f'{self.date_joined.strftime("%Y-%m-%d ")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        return [self.get_number(), self.status, self.user.username,
                date_joined, date_process, date_end_process, self.efficiency, self.id]

    class Meta:
        verbose_name = 'Production'
        verbose_name_plural = 'Productions'
        ordering = ['-id']


class ProductionShopping(models.Model):
    production = models.ForeignKey(production, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def toJSONPROCESS(self):
        item = model_to_dict(self)
        item['id_shopping'] = self.shopping_cart.id
        item['shopping_name'] = self.shopping_cart.__str__()
        item['id_product'] = self.product_id
        item['product_name'] = self.product.__str__()
        item['value'] = item['product_name']
        available = self.shopping_cart.shoppingdetail_set.get(product_id=self.product_id)
        item['available'] = available.available
        item['cant'] = self.cant
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item


class detail_production(models.Model):
    production = models.ForeignKey(production, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # type = models.CharField(max_length=2, choices=type_product, verbose_name='Tipo de producción')
    cant = models.IntegerField(default=0)

    def toJSON(self):
        item = model_to_dict(self)
        item['product_id'] = self.product.id
        item['product'] = f'{self.product.code} - {self.product.name}  {self.product.um}'
        item['category'] = self.product.category.name
        return item

    class Meta:
        verbose_name = 'Detalle de produccion'
        verbose_name_plural = 'Detalle de producciones'
        default_permissions = ()
        ordering = ['id']


class specifications(models.Model):
    production = models.ForeignKey(production, on_delete=models.CASCADE)
    health_certificate = models.FileField(upload_to='healthCertificate', verbose_name='Certificado sanitario')
    characteristics = models.FileField(upload_to='characteristics', verbose_name='Características')
    chemical_analysis = models.FileField(upload_to='chemical_analysis', verbose_name='Análisis químico')

    # Quitar esta parte y se agregra en caracteristicas
    # purity = models.CharField(max_length=15, verbose_name='% de pureza')
    # humidity = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='% humedad')

    def __str__(self):
        return f'{self.production_id} - {self.characteristics}'

    def get_chemical_analysis_file(self):
        if self.chemical_analysis:
            return '{}{}'.format(settings.MEDIA_URL, self.chemical_analysis)
        else:
            return 'No insertado'

    def get_health_certificate_file(self):
        if self.health_certificate:
            return '{}{}'.format(settings.MEDIA_URL, self.health_certificate)
        return 'No insertado'

    def get_characteristics_file(self):
        if self.characteristics:
            return '{}{}'.format(settings.MEDIA_URL, self.characteristics)
        return 'No insertado'

    def toJSON(self):

        item = model_to_dict(self)
        item['Lot number'] = self.production.id
        item['Product'] = self.production.detail_production_set.filter(product__category__name='PF')
        item['Production Date'] = self.production.date_joined.strftime('%d %b %Y')
        item['Characteristics'] = self.get_characteristics_file()
        item['Chemical analysis'] = self.get_chemical_analysis_file()
        item['Health certificate'] = self.get_health_certificate_file()
        return item

    def toLIST(self):
        data = [self.id, self.production.id, self.production.date_joined, self.get_health_certificate_file(),
                self.get_characteristics_file(), self.get_chemical_analysis_file(), self.id]
        return data

    class Meta:
        verbose_name = 'Especificacion de produccion'
        verbose_name_plural = 'Especificacion de producciones'
        ordering = ['id']
