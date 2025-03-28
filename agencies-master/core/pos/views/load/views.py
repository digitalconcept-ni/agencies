import csv
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView

from core.pos.choices import random_code
from core.pos.models import Product, Brands, Category, ProductWarehouse, Warehouse


class loadCsvView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'load/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            selection = request.POST['selection']
            update = request.POST['update']
            file = request.FILES['file']
            decode_file = file.read().decode("utf-8-sig").splitlines()
            reader = csv.reader(decode_file, delimiter=';')

            if selection == "ajuste":
                ProductWarehouse.objects.all().delete()
                warehouse = Warehouse(
                    code="3000",
                    name="CENTRAL",
                    description='BODEGA CENTRAL',
                    status=1,
                    is_central=1
                ).save()

                products = Product.objects.select_related()

                pw_update = []
                for p in products:
                    pw = ProductWarehouse(
                        warehouse=warehouse.id,
                        product_id=p.id,
                        stock=p.stock,
                    )
                    pw_update.append(pw)

                ProductWarehouse.objects.bulk_create(pw_update)

                data['success'] = 'Bodega Eliminada correctamente'
            if selection == 'category':
                category_update = []
                for row in reader:
                    cat = Category(
                        name=row[0].strip(),
                        desc='',
                    )
                    category_update.append(cat)
                Category.objects.bulk_create(category_update)
                # Category.objects.filter(name='', desc='').delete()
                data['success'] = 'Categorias grabadas exitosamente'
            elif selection == 'product':
                product_list = []

                if update == 'true':
                    print('update')
                    product = Product()

                else:
                    for row in reader:
                        print(row)
                        if row[6] == '':
                            value = 0.00
                        else:
                            value = float(row[6])

                        product = Product(
                            # supplier_id=row[0],
                            brand_id=row[0],
                            category_id=row[1],
                            name=row[2],
                            code=row[3],
                            tax=row[4],
                            um=row[5],
                            is_inventoried=True,
                            stock=int(row[6]),
                            cost=value,
                            pvp=float(row[8])
                        )
                        product_list.append(product)
                    Product.objects.bulk_create(product_list)
                    data['success'] = 'Proceso terminado con exito'
            elif selection == 'brands':
                brand_list = []
                for row in reader:
                    print(row)
                    brand = Brands(
                        name=row[0].strip(),
                        description=row[1].strip()
                    )
                    brand_list.append(brand)
                Brands.objects.bulk_create(brand_list)
                # Brands.objects.filter(name='', description='').delete()
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
