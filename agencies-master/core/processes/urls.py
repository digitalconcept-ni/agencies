from django.urls import path

from core.processes.views.production.view import *
from core.processes.views.specifications.views import *

urlpatterns = [
    # production
    path('production/', ProductionListView.as_view(), name='production_list'),
    path('production/add/', ProductionCreateView.as_view(), name='production_add'),
    path('production/update/<int:pk>/', ProductionUpdateView.as_view(), name='production_update'),

    # Specifications
    path('specifications/', SpecificationsListView.as_view(), name='specifications_list'),
    path('specifications/add/', SpecificationsCreateView.as_view(), name='specifications_add'),

    # La visualizacion de los QR se lanzara a la raiz para ocultar las URLs

]
