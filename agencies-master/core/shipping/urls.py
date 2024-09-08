from django.urls import path

from core.shipping.views.deliveries.views import *
from core.shipping.views.vehicles.views import *

urlpatterns = [
    # vehicles
    path('vehiculos/', VehiclesListView.as_view(), name='vehicles_list'),
    path('vehiculos/add/', VehiclesCreateView.as_view(), name='vehicles_add'),
    path('vehiculos/update/<int:pk>/', VehiclesUpdateView.as_view(), name='vehicles_update'),

    # Deliveries
    path('entregas/', DeliveriesListView.as_view(), name='deliveries_list'),
    path('entregas/add/', DeliveriesCreateView.as_view(), name='deliveries_add'),
    path('entregas/update/<int:pk>/', DeliveriesUpdateView.as_view(), name='deliveries_update'),
]
