import csv
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView

from core.pos.choices import random_code
from core.pos.models import Product, Brands


class loadCsvView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'load/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            selection = request.POST['selection']
            if selection == 'product':
                print('products')
                product_list = []
                file = request.FILES['file']
                decode_file = file.read().decode("utf-8").splitlines()
                reader = csv.reader(decode_file)
                for row in reader:
                    product = Product(
                        # supplier_id=row[0],
                        brand_id=row[0],
                        category_id=row[1],
                        name=row[2],
                        code=random_code(),
                        um=row[3],
                        expiration=row[4],
                        image='',
                        is_inventoried=True,
                        stock=row[5],
                        cost=row[6],
                        pvp=row[7]
                    )
                    product_list.append(product)
                Product.objects.bulk_create(product_list)
                data['success'] = 'Proceso terminado con exito'
            elif selection == 'brands':
                brand_list = []
                file = request.FILES['file']
                decode_file = file.read().decode("utf-8").splitlines()
                reader = csv.reader(decode_file)

                for row in reader:
                    brand = Brands(
                        name=row[0],
                        description=row[1]
                    )
                    brand_list.append(brand)
                Brands.objects.bulk_create(brand_list)
                data['success'] = 'Marcas grabadas exitosamente'

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
