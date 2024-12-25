import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField, Q, F, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.pos.models import Sale, Product, SaleProduct, Client, Company
from core.pos.query import visitFrequency
from core.processes.models import production
from core.user.models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def graph(self):
        data = []
        # QUERY GRAPH COLUM BAR graphcolumn
        graphColumnPoints = []
        year = datetime.now().year
        for m in range(1, 13):
            total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
            graphColumnPoints.append(float(total))
        graphcolumn = {
            'name': 'Porcentaje de venta',
            'showInLegend': False,
            'colorByPoint': True,
            'data': graphColumnPoints
        }

        graphPiePoints = []
        year = datetime.now().year
        month = datetime.now().month
        for p in Product.objects.filter():
            total = SaleProduct.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
                                               product_id=p.id).aggregate(
                result=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('result')
            if total > 0:
                graphPiePoints.append({'name': p.name, 'y': float(total)})
        graphpie = {
            'name': 'Porcentaje',
            'colorByPoint': True,
            'data': graphPiePoints
        }

        data.append({'graphcolumn': graphcolumn})
        data.append({'graphpie': graphpie})
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        try:
            data = {}
            now = datetime.now()
            action = request.POST['action']
            if action == 'search_investment':
                if request.user.is_superuser:
                    investment = Product.objects.select_related().aggregate(
                        result=Coalesce(Sum(F('stock') * F('cost')), 0.00, output_field=FloatField())).get('result')
                    pvp = Product.objects.all().aggregate(
                        result=Coalesce(Sum(F('stock') * F('pvp')), 0.00, output_field=FloatField())).get('result')
                    revenue = float(pvp) - float(investment)
                    data = [[1, f'{investment:,.2f}', f'{revenue:,.2f}']]
                else:
                    data['error'] = 'No tiene acceso a esta informacion'
            elif action == 'search_data':

                prod = production.objects.select_related()
                prod_detail = {
                    'process-lot': prod.filter(status=False).count(),
                    'finaly-lot': prod.filter(status=True).count(),
                    'total-lot': prod.count()
                }

                maximumProductSold = SaleProduct.objects.select_related().filter(sale__date_joined=now).values(
                    'product__name').annotate(
                    total=Sum(F('cant'))).order_by('-total')[:5]
                sold = []
                for x, maximumProductSold in enumerate(maximumProductSold):
                    sold.append([x + 1, maximumProductSold['product__name'], maximumProductSold['total']])

                queryProducts = Product.objects.select_related()
                querySales = Sale.objects.select_related()
                if request.user.is_superuser:
                    sale = querySales.filter(date_joined__exact=now)
                else:
                    sale = querySales.filter(Q(user_id=request.user.id) & Q(date_joined__exact=now))
                lowInventory = queryProducts.filter(stock__lte=15).count()
                totalProductsQuery = queryProducts.count()
                totalClientsQuery = Client.objects.count()
                countSalesToday = sale.count()
                countSalesTodayMoney = sale.aggregate(
                    result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get('result')
                appliedCredit = querySales.filter(Q(payment='credit') & Q(applied=False)).count()

                data = {
                    'sales': countSalesToday,
                    'amount': countSalesTodayMoney,
                    'products': totalProductsQuery,
                    'clients': totalClientsQuery,
                    'lower-inventory': lowInventory,
                    'maximumsold': sold,
                    'programing-clients': visitFrequency(request).count(),
                    'applied-credit': appliedCredit,
                    'prod': prod_detail,
                }
            elif action == 'search_presale_info':
                today = str(now.date())
                data = []
                exist = User.objects.filter(presale=True).exists()
                if exist:
                    query = visitFrequency(request)
                    cantProgramingCLients = query.filter(user__presale=True).values('user__username').annotate(
                        client=Count(F('id')))
                    cantSales = query.filter(Q(sale__date_joined=today) & Q(user__presale=True)).values(
                        'user__username').annotate(sale=Coalesce(Count('id'), 0))

                    presales = [i.get('user__username') for i in cantSales]

                    cpGeneral = 0  # Total clients programs today
                    ceGeneral = 0  # Total effectiveness clients

                    for s in cantProgramingCLients:
                        if s['user__username'] in presales:
                            i = presales.index(s['user__username'])
                            sale = int(cantSales[i]['sale'])
                            effectiveness = (sale * 100) / s['client']
                            data.append([1, s['user__username'], s['client'],
                                         sale, effectiveness])
                            ceGeneral += sale
                        else:
                            effectiveness = (0 * 100) / s['client']
                            data.append([1, s['user__username'], s['client'],
                                         0, effectiveness])
                        cpGeneral += s['client']

                    eGeneral = (ceGeneral * 100) / cpGeneral
                    data.append([1, '--------', cpGeneral, ceGeneral, eGeneral])
                else:
                    data = {'info': 'No hay pre ventas activos para calcular el reporte'}
                    return JsonResponse(data, safe=False)
            elif action == 'search_lower_inventory':
                queryProducts = Product.objects.filter(stock__lte=10)
                data = [p.toLIST() for p in queryProducts]
                # for p in queryProducts:
                #     data.append([p.id, p.name, p.brand.name, p.stock,
                #                  f'{p.cost:.2f}'])
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
            elif action == 'view-credit-noapplied':
                appliedCredit = Sale.objects.filter(Q(payment='credit') & Q(applied=False))
                data = []
                total = 0
                for i in appliedCredit:
                    total += f'{i.total:,.2f}'
                    data.append([i.id, i.purchase_order, i.user.username, i.client.names, i.end, f'{i.total:,.2f}'])
                data.append(['--', '----', '----', '----', 'Total', f'{total:,.2f}'])
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BisB -Dashboard'
        context['panel'] = 'Panel de administrador'
        context['create_url'] = reverse_lazy('shopping_create')
        context['sales_url'] = reverse_lazy('sale_list')
        context['clients_url'] = reverse_lazy('client_list')
        context['graph'] = self.graph()
        return context


def page_not_found404(request, exception):
    return render(request, '404.html')
