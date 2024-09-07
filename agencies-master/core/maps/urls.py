from django.urls import path

from core.maps.views import MapListView

urlpatterns = [
    # dashboard
    path('', MapListView.as_view(), name='client_maps'),
]
