from django.db import models
from django.forms import model_to_dict

from core.pos.models import Sale

# Create your models here.

vehicles = (
    ('car', 'Carro'),
    ('motorcicle', 'Motocicleta'),
    ('ship', 'Barco'),
    ('truck', 'Camión'),
    ('plane', 'Avión'),
)


class vehicles(models.Model):
    name = models.CharField(choices=vehicles, max_length=11, verbose_name='Nombre Vehiculo')
    driver = models.CharField(max_length=50, verbose_name='Conductor')
    vehicle_registration = models.CharField(max_length=7, verbose_name='Nro placa')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Fecha registro')

    def __str__(self):
        return f'{self.name} {self.driver}'

    def toLIST(self):
        name = self.get_name_display()
        item = [
            self.id, name, self.driver, self.vehicle_registration, self.date_joined, self.id
        ]
        return item

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'vehiculo'
        verbose_name_plural = 'vehiculos'
        ordering = ['-date_joined']


class deliveries(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')
    vehicle = models.ForeignKey(vehicles, on_delete=models.CASCADE, verbose_name='Vehiculo')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Fecha registro')
    shipping_date = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name="Fecha Envio")
    delivery_date = models.DateField(auto_now_add=False, null=True, blank=True, verbose_name='Fecha entrega')
    amount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Costo envio")
    initial_km = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name="Kilometro inicial")
    final_km = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name="Kilometro final")
    total_distance = models.DecimalField(default=0.00, max_digits=5, decimal_places=2,
                                         verbose_name="Distancia recorrida")
    status = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_distance = self.final_km - self.initial_km
        super(deliveries, self).save()

    def toLIST(self):
        kmi = f'{self.initial_km:.2f}'
        kmf = f'{self.final_km:.2f}'
        amount = f'{self.amount:.2f}'
        if self.shipping_date and self.delivery_date:
            shipping_date = self.shipping_date.strftime("%Y-%m-%d")
            delivery_date = self.delivery_date.strftime("%Y-%m-%d")
        else:
            shipping_date = 'Pendiente de ingreso'
            delivery_date = 'Pendiente de ingreso'
        total_distance = f'{self.total_distance:.2f}'
        sale = f'{self.sale.get_number()} {self.sale.client.get_full_name()}'
        item = [
            self.id, f'{self.date_joined.strftime("%Y-%m-%d")}', sale, self.vehicle.__str__(),
            shipping_date, delivery_date, amount, kmi,
            kmf, total_distance, self.status, self.id
        ]
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item["vehicle"] = self.vehicle.toJSON()
        return item

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-shipping_date']
