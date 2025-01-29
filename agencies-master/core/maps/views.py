import json

from django.views.generic import FormView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Client
from core.reports.forms import ReportForm


# Create your views here.

class MapListView(ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'map/load.html'
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

    # def getClientsPoints(self):
    #     try:
    #         data = []
    #         errors = []  # Lista para almacenar errores
    #         query = Client.objects.filter(is_active=True)
    #         for i in query:
    #             # Validamos si las coordenadas no son de tipo float
    #             # Si no lo son las pasamos a float para su validacion
    #             if i.lat not in [None, 'undefined'] or i.lng not in [None, 'undefined']:
    #                 cleaned_value = i.lat.strip().rstrip('.')
    #                 cleaned_value != '' and cleaned_value.replace('.', '', 1).isdigit()
    #                 lat = float(i.lat)
    #                 lng = float(i.lng)
    #                 if self.is_valid_coordinate(lat, lng):
    #                     data.append(i.toJSON())
    #     except ValueError as e:
    #         data = {'error': str(e)}
    #     return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        # try:
        #     action = request.POST['action']
        #     if action == 'apply_credit':
        #         s = Sale.objects.get(id=request.POST['id'])
        #         s.applied = True
        #         s.save()
        #     elif action == 'download_guides':
        #         data = []
        #         param = {
        #             'id': request.POST['id'],
        #             'tenant': request.tenant.schema_name,
        #             'user': request.user,
        #             'uri': request.build_absolute_uri(),
        #             'session': request.session,
        #         }
        #         path = self.guide(param)
        #         data = path
        #     elif action == 'search':
        #         data = []
        #         start_date = request.POST['start_date']
        #         end_date = request.POST['end_date']
        #         queryset = Sale.objects.select_related()
        #         if len(start_date) and len(end_date) and request.user.is_superuser:
        #             queryset = queryset.filter(date_joined__range=[start_date, end_date])
        #         elif len(start_date) and len(end_date) and not request.user.is_superuser:
        #             queryset = queryset.filter(
        #                 Q(user_id=request.user.id) & Q(date_joined__range=[start_date, end_date]))
        #         elif not len(start_date) and not len(end_date) and not request.user.is_superuser:
        #             queryset = queryset.filter(user_id=request.user.id)
        #
        #         for i in queryset:
        #             data.append(i.toLIST())
        #     elif action == 'search_products_detail':
        #         data = []
        #         for i in SaleProduct.objects.filter(sale_id=request.POST['id']):
        #             data.append(i.toJSON())
        #     elif action == 'delete':
        #         sale = Sale.objects.get(id=request.POST['id'])
        #         set = sale.saleproduct_set.all()
        #         for s in set:
        #             s.product.stock += s.cant
        #             s.save()
        #         sale.delete()
        #     else:
        #         data['error'] = 'No se ha encontrado el action'
        # except Exception as e:
        #     # print(str(e))
        #     data['error'] = str(e)
        # return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mapa de clientes'
        context['points'] = self.getClientsPoints()
        # context['create_url'] = reverse_lazy('sale_create')
        # context['list_url'] = reverse_lazy('sale_list')
        context['entity'] = 'Mapa'
        # context['pre_sales'] = User.objects.filter(presale=True)
        return context
