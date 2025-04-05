import json

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Client
from core.reports.forms import ReportForm


# Create your views here.

class MapListView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = ReportForm
    template_name = 'map/map.html'
    permission_required = 'view_sale'

    def is_valid_coordinate(self, lat, lng):
        """
        Verifica si las coordenadas son válidas.

        Args:
            lat (float): Latitud a verificar.
            lng (float): Longitud a verificar.

        Returns:
            bool: True si las coordenadas son válidas, False en caso contrario.
        """
        # Verificar que las coordenadas sean números
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            return False

        # Verificar el rango de las coordenadas
        return -90 <= lat <= 90 and -180 <= lng <= 180

    # Funcion para obtener los PDV

    def getClientsPoints(self):
        data = []
        errors = []  # Lista para almacenar errores

        query = Client.objects.filter(is_active=True)
        for i in query:
            try:
                # Validamos si las coordenadas no son de tipo float
                # Si no lo son, las pasamos a float para su validación
                if i.lat not in [None, 'undefined'] and i.lng not in [None, 'undefined']:
                    cleaned_value = i.lat.strip().rstrip('.')
                    if cleaned_value != '' and cleaned_value.replace('.', '', 1).isdigit():
                        lat = float(i.lat)
                        lng = float(i.lng)
                        if self.is_valid_coordinate(lat, lng):
                            data.append(i.toJSON())
                    else:
                        errors.append({'id': i.id, 'error': 'Coordenadas no válidas'})
                else:
                    errors.append({'id': i.id, 'error': 'Coordenadas no definidas'})
            except ValueError as e:
                errors.append({'id': i.id, 'error': str(e)})

        # Si hay errores, los incluimos en la respuesta
        if errors:
            return json.dumps({'data': data, 'errors': errors})

        return json.dumps({'data': data})

    def post(self, request, *args, **kwargs):
        data = {}
        # leemos la infomraicon que desde la vista de los mapas
        info = json.loads(request.body)
        try:
            if info['action'] == 'client-detail':
                request.session['client_data'] = info.get('client', {'ll': 'no paso nada'})
                # print("Datos guardados en la sesión:", request.session['client_data'])
                # data['url'] = reverse_lazy('client-detail', kwargs={'pk': request.session['client_data']['id']})
                # return reverse_lazy('client-detail', kwargs={'pk': request.session['client_data']['id']})
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mapa de clientes'
        context['points'] = self.getClientsPoints()
        context['entity'] = 'Mapa'
        return context


class MapClientDetailView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "map/client-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_data = self.request.session.get('client_data', {})
        query = Client.objects.select_related().get(id=client_data['id'])
        context['client'] = query
        context['title'] = 'Detalle del cliente'
        context['map_url'] = reverse_lazy('map')
        return context
