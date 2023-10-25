from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField, Q, F, Func, Count, Max
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.pos.models import Sale, Product, SaleProduct, Client
from core.user.models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            now = datetime.now()
            action = request.POST['action']
            if action == 'search_investment':
                if request.user.is_superuser:
                    investment = Product.objects.all().aggregate(
                        result=Coalesce(Sum(F('stock') * F('cost')), 0.00, output_field=FloatField())).get('result')
                    pvp = Product.objects.all().aggregate(
                        result=Coalesce(Sum(F('stock') * F('pvp')), 0.00, output_field=FloatField())).get('result')
                    revenue = float(pvp) - float(investment)
                    data = [[1, f'{investment:.2f}', f'{revenue:.2f}']]
                else:
                    data['error'] = 'No tiene acceso a esta informacion'
            elif action == 'search_data':
                maximumProductSold = SaleProduct.objects.select_related().filter(sale__date_joined=now).values(
                    'product__name').annotate(
                    total=Sum(F('cant'))).order_by('-total')[:5]
                sold = []
                for x, maximumProductSold in enumerate(maximumProductSold):
                    sold.append([x + 1, maximumProductSold['product__name'], maximumProductSold['total']])

                queryProducts = Product.objects.select_related()
                querySales = Sale.objects.select_related().filter(date_joined__exact=now)
                if request.user.is_superuser:
                    sale = querySales
                else:
                    sale = querySales.filter(user_id=request.user.id)
                lowInventory = queryProducts.filter(stock__lte=15).count()
                totalProductsQuery = queryProducts.count()
                totalClientsQuery = Client.objects.count()
                countSalesToday = sale.count()
                countSalesTodayMoney = sale.aggregate(
                    result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get('result')

                data = {
                    'sales-today': countSalesToday,
                    'sales': countSalesTodayMoney,
                    'products': totalProductsQuery,
                    'clients': totalClientsQuery,
                    'lower-inventory': lowInventory,
                    'maximumsold': sold
                }
            elif action == 'search_lower_inventory':
                queryProducts = Product.objects.filter(stock__lte=10)
                data = []
                for p in queryProducts:
                    data.append([p.id, p.name, p.category.name, p.stock,
                                 f'{p.cost:.2f}'])
            elif action == 'search_payment_method':
                data = []
                query = Sale.objects.select_related().filter(date_joined=now)
                cashPayment = query.filter(payment='cash')
                creditPayment = query.filter(payment='credit')
                posPayment = query.filter(payment='pos')
                transferPayment = query.filter(payment='trasnfer')

                cash = cashPayment.aggregate(result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get(
                    'result')
                credit = creditPayment.aggregate(result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get(
                    'result')
                pos = posPayment.aggregate(result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get(
                    'result')
                transfer = transferPayment.aggregate(
                    result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get('result')

                data.append(
                    [1, [cashPayment.count(), cash], [posPayment.count(), pos], [transferPayment.count(), transfer],
                     [creditPayment.count(), credit]])
                # data.append(
                #     [1, cashPayment.count(), posPayment.count(), transferPayment.count(), creditPayment.count()])

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
        context['title'] = 'BisB -Dashboard'
        context['panel'] = 'Panel de administrador'
        context['create_url'] = reverse_lazy('shopping_create')
        context['sales_url'] = reverse_lazy('sale_list')
        context['clients_url'] = reverse_lazy('client_list')
        return context


def page_not_found404(request, exception):
    return render(request, '404.html')
