from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from core.pos.models import Product, Client
from core.user.models import User

position = (
    ('SL', 'SOLDADOR'),
    ('PN', 'PINTOR'),
    ('TR', 'TORNERO'),
)


class Technicians(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(choices=position, max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)

    def __str__(self):
        return f'{self.name} - {self.get_position_display()}'

    def toJSON(self):
        item = model_to_dict(self)
        item['position'] = self.get_position_display()
        return item

    def toLIST(self):
        position = self.get_position_display()
        dateTime = f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        item = [
            self.id, self.name, position, self.user.username, dateTime, self.id]
        return item

    class Meta:
        verbose_name = 'technical'
        verbose_name_plural = 'technicians'
        ordering = ['-date_joined']


class Exits(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technicians, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)

    def __str__(self):
        dateTime = f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        return f'{self.technician.name} - {self.technician.get_position_display()} - {dateTime}'

    def toLIST(self):
        technician = f'{self.technician.name} - {self.technician.get_position_display()}'
        dateTime = f'{self.date_joined.strftime("%Y-%m-%d")} - {self.time_joined.strftime("%I:%M:%S %p")}'
        item = [
            self.id, self.client.names, technician, self.status, self.user.username, dateTime, self.id
        ]
        return item

    class Meta:
        verbose_name = 'exit'
        verbose_name_plural = 'exits'
        ordering = ['-date_joined']


class ExitsDetail(models.Model):
    exit = models.ForeignKey(Exits, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)
    restore = models.BooleanField(default=False, verbose_name='Retorno')

    # joined = models.BooleanField(default=False, verbose_name='Agregado')

    # def __str__(self):
    #     return self.cliente

    def toJSON(self):
        item = model_to_dict(self)
        item['product_id'] = self.product.id
        item['category'] = self.product.category.name
        item['product'] = self.product.__str__()
        return item

    def toLIST(self):
        item = [
            self.id, self.product.__str__(), self.cant, self.restore
        ]
        return item

    class Meta:
        verbose_name = 'ExitDetail'
        verbose_name_plural = 'ExitsDetails'
        ordering = ['id']
