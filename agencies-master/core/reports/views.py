from datetime import datetime

from django.db.models import Sum, FloatField, Q, F
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Sale, SaleProduct
from core.reports.forms import ReportForm
from core.user.models import User


class ReportSaleView(ValidatePermissionRequiredMixin, FormView):
    template_name = 'sale/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_sale':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                queryset = Sale.objects.select_related()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for s in queryset:
                    data.append([
                        s.id,
                        s.client.names,
                        s.date_joined.strftime('%Y-%m-%d'),
                        f'{s.subtotal:.2f}',
                        f'{s.total_iva:.2f}',
                        f'{s.total:.2f}',
                    ])

                subtotal = queryset.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('r')
                iva = queryset.aggregate(r=Coalesce(Sum('total_iva'), 0, output_field=FloatField())).get('r')
                total = queryset.aggregate(r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    f'{subtotal:.2f}',
                    f'{iva:.2f}',
                    f'{total:.2f}',
                ])
            elif action == 'search_presale_info':
                now = datetime.now()
                query = Sale.objects.select_related().filter(Q(date_joined__exact=now) & Q(user_id=request.POST['id']))
                if query.count() != 0:
                    totalMoney = query.aggregate(result=Sum(F('total'))).get('result')
                    totalSales = query.count()
                    u = query.order_by('time_joined').last()
                    data = [[request.POST['id'], f'{totalSales}', f'{totalMoney:.2f}', f'{u.client.names}',
                             f'{u.time_joined.strftime("%H:%M:%S")}']]
                    print(data)
                else:
                    data['info'] = 'No se encontraron ventas de hoy'
            elif action == 'search_sale_presale':
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                presale = request.POST.get('presale', '')
                query = SaleProduct.objects.select_related().filter(sale__date_joined__range=[start_date, end_date])
                sold = []

                if presale == 'all':
                    subQuery = query.values('product__name', 'product__brand__name').annotate(
                        total=Sum(F('cant'))).order_by('-total')
                else:
                    subQuery = query.filter(sale__user_id=presale).values(
                        'sale__user__username', 'product__name', 'product__brand__name').annotate(
                        total=Sum(F('cant'))).order_by('-total')
                    presaleNmae = subQuery.values('sale__user__username')[1]
                    sold.append([0, '------', '------', presaleNmae.get('sale__user__username')])
                for x, subQuery in enumerate(subQuery):
                    sold.append([x + 1, subQuery['product__brand__name'], subQuery['product__name'], subQuery['total']])
                data = sold
                # now = datetime.now()
                # if query.count() != 0:
                #     totalMoney = query.aggregate(result=Sum(F('total'))).get('result')
                #     totalSales = query.count()
                #     u = query.order_by('time_joined').last()
                #     data = [[request.POST['id'], f'{totalSales}', f'{totalMoney:.2f}', f'{u.client.names}',
                #              f'{u.time_joined.strftime("%H:%M:%S")}']]
                #     print(data)
                # else:
                #     data['info'] = 'No se encontraron ventas de hoy'
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reportes'
        context['entity'] = 'Reportes'
        context['pre_sales'] = User.objects.filter(presale=True)
        context['list_url'] = reverse_lazy('sale_report')
        return context
