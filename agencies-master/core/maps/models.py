from django.db import models
from django.forms import model_to_dict

from core.pos.models import Client
from core.user.models import User
from core.user.storage_backends import TenantS3Storage


# Create your models here.

class Zone(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, verbose_name='Código zona')
    name = models.CharField(max_length=100, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        ordering = ['code']

    def __str__(self):
        return f'{self.supervisor} | {self.code} {self.name}'

    def toLIST(self):
        user = f'{self.supervisor.first_name} {self.supervisor.last_name}'
        item = [
            self.id, self.code, user, self.name
        ]
        return item


class Route(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    presale = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, verbose_name='Código ruta')

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['zone']

    def __str__(self):
        return f'{self.zone.code} | {self.code} {self.presale}'

    def toLIST(self):
        user = f'{self.presale.first_name} {self.presale.last_name}'
        item = [
            self.id, self.zone.__str__(), self.code, user
        ]
        return item


class ModuloDayVisit(models.Model):
    DAYS_WEEK = (
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
    )
    day = models.IntegerField(choices=DAYS_WEEK, unique=True,
                              verbose_name='Dias de visita')  # Ejemplo: 'Lunes', 'Martes', etc.

    def __str__(self):
        return self.get_day_display()

    class Meta:
        verbose_name = 'Dia de visita'
        verbose_name_plural = 'Días de visita'
        ordering = ['day']


class Modulo(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Ruta')
    code = models.CharField(max_length=100, verbose_name='Código modulo')
    ubigeo = models.CharField(max_length=100, verbose_name='zonas a visitar')
    limits = models.FileField(storage=TenantS3Storage(), upload_to='limits/', verbose_name='Limites de ruta')
    days = models.ManyToManyField(ModuloDayVisit, verbose_name='Días de visita')

    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
        ordering = ['code']

    def __str__(self):
        return f'{self.route.__str__()} | {self.code} {self.ubigeo}'

    def getLimitsFile(self):
        if self.limits:
            return f'{self.limits}'
        return None

    def toLIST(self):
        item = [
            self.id, self.route.__str__(), self.code, self.ubigeo, self.getLimitsFile()
        ]
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item['limits'] = self.getLimitsFile()
        return item

    def save(self, *args, **kwargs):
        if self.pk:
            pass
        super().save(*args, **kwargs)  # Guarda el modelo


class Visit(models.Model):
    presale = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # ruta = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    checkin = models.TimeField()
    checkout = models.TimeField()
    duracion_negociacion = models.IntegerField()  # Duración en minutos

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['presale', 'date']
