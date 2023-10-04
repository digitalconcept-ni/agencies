from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField, Q, F, Func
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.pos.models import Sale, Product, SaleProduct, Client


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_investment':
                if request.user.is_superuser:
                    investment = Product.objects.all().aggregate(
                        result=Coalesce(Sum(F('stock') * F('cost')), 0.00, output_field=FloatField())).get('result')
                    pvp = Product.objects.all().aggregate(
                        result=Coalesce(Sum(F('stock') * F('pvp')), 0.00, output_field=FloatField())).get('result')
                    revenue = float(pvp) - float(investment)
                    data = [[1, f'{investment:.2f}', f'{revenue:.2f}']]
                    print(data)
                else:
                    data['error'] = 'No tiene acceso a esta informacion'
            elif action == 'search_cards_data':
                now = datetime.now()
                if request.user.is_superuser:
                    query = Sale.objects.filter(date_joined__exact=now).only('total')
                else:
                    query = Sale.objects.filter(Q(date_joined__exact=now) & Q(user_id=request.user.id)).only('total')
                queryProducts = Product.objects.filter(stock__lte=10).count()
                totalProductsQuery = Product.objects.count()
                totalClientsQuery = Client.objects.count()
                countSalesNow = 0
                countSalesNowMoney = 0

                for i in query:
                    countSalesNowMoney += i.total
                    countSalesNow += 1
                data = {
                    'sales-today': countSalesNow,
                    'sales': countSalesNowMoney,
                    'products': totalProductsQuery,
                    'clients': totalClientsQuery,
                    'lower-inventory': queryProducts,
                }
            elif action == 'search_lower_inventory':
                queryProducts = Product.objects.filter(stock__lte=10)
                data = []
                for p in queryProducts:
                    data.append([p.id, p.name, p.category.name, p.stock,
                                 f'{p.cost:.2f}'])
            elif action == 'get_graph_sales_year_month':
                points = []
                year = datetime.now().year
                for m in range(1, 13):
                    total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                        result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    points.append(float(total))
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': points
                }
            elif action == 'get_graph_sales_products_year_month':
                points = []
                year = datetime.now().year
                month = datetime.now().month
                for p in Product.objects.filter():
                    total = SaleProduct.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
                                                       product_id=p.id).aggregate(
                        result=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('result')
                    if total > 0:
                        points.append({'name': p.name, 'y': float(total)})
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': points
                }
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BISB - HOME | DASCHBOARD'
        context['panel'] = 'Panel de administrador'
        context['create_url'] = reverse_lazy('shopping_create')
        context['sales_url'] = reverse_lazy('sale_list')
        context['clients_url'] = reverse_lazy('client_list')
        return context


def page_not_found404(request, exception):
    return render(request, '404.html')
