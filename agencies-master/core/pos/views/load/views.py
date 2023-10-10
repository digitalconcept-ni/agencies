import csv
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView

from core.pos.models import Product


class loadCsvView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'load/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'insert_file':
                print('entry the action')
                product_list = []
                file = request.FILES['file']
                decode_file = file.read().decode("utf-8").splitlines()
                reader = csv.reader(decode_file)
                for row in reader:
                    product = Product(
                        name=row[0],
                        code=row[1],
                        category_id=row[4],
                        image='',
                        is_inventoried=True,
                        stock=row[2],
                        cost=row[5],
                        pvp=row[3]
                    )
                    product_list.append(product)
                Product.objects.bulk_create(product_list)
                data['success'] = 'Proceso terminado con exito'
            return JsonResponse(data, safe=False)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carga masiva'
        # context['create_url'] = reverse_lazy('client_create')
        # context['list_url'] = reverse_lazy('client_list')
        context['entity'] = 'load'
        return context
