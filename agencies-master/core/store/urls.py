from django.urls import path

from core.store.views.exits.view import ExitsListView, ExitsCreateView, ExitsUpdateView
from core.store.views.technicians.views import *

urlpatterns = [
    # Technicians
    path('technicians/', TechnicansListView.as_view(), name='technicans_list'),
    path('technicians/add/', TechnicansCreateView.as_view(), name='technicans_create'),

    # Exits
    path('exits/', ExitsListView.as_view(), name='exits_list'),
    path('exits/add/', ExitsCreateView.as_view(), name='exits_create'),
    path('exits/update/<int:pk>/', ExitsUpdateView.as_view(), name='exits_create'),
]
