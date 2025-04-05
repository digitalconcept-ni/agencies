from django.urls import path

from core.maps.views.map.views import MapListView, MapClientDetailView
from core.maps.views.modulo.views import ModuloListView, ModuloCreateView, ModuloUpdateView
from core.maps.views.route.views import RouteListView, RouteCreateView, RouteUpdateView
from core.maps.views.zone.views import *

urlpatterns = [
    # Visualizacion del mapa
    path('', MapListView.as_view(), name='map'),
    # Detalle del cliente
    path('client-detail/', MapClientDetailView.as_view(), name='client-detail'),

    # Zone
    path('zone/', ZoneListView.as_view(), name='zone_list'),
    path('zone/create/', ZoneCreateView.as_view(), name='zone_create'),
    path('zone/update/<int:pk>/', ZoneUpdateView.as_view(), name='zone_update'),

    # Route
    path('route/', RouteListView.as_view(), name='route_list'),
    path('route/create/', RouteCreateView.as_view(), name='route_create'),
    path('route/update/<int:pk>/', RouteUpdateView.as_view(), name='route_update'),

    # Modulo
    path('modulo/', ModuloListView.as_view(), name='modulo_list'),
    path('modulo/create/', ModuloCreateView.as_view(), name='modulo_create'),
    path('modulo/update/<int:pk>/', ModuloUpdateView.as_view(), name='modulo_update'),
]
