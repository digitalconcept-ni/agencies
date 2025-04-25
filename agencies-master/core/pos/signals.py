from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.pos.models import Company

'''
Signal que nos ayudara a saber cuando el modelo company se ha actualizado
para invalidar la cache actual y asignarle los nuevos valores
'''


@receiver(post_save, sender=Company)
def PostsaveCompany(sender, instance, created, **kwargs):
    key = f'cache_{instance.tenant.id}'
    if not created:
        cache.set(key, f'{instance.control_stock}')  # Agregamos los nuevos valores a la cache
    # if created:
    #     print(f"La configuración del cliente '{instance}' con ID {instance.pk} fue creada.")
    #     # Aquí podrías realizar acciones específicas para la creación
    # else:
    #     print(f"La configuración del cliente '{instance}' con ID {instance.pk} fue actualizada.")
    # Aquí podrías realizar acciones específicas para la actualización
