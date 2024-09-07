from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.processes.forms import SpecificationsForm
from core.processes.models import specifications


class SpecificationsListView(ValidatePermissionRequiredMixin, ListView):
    model = specifications
    template_name = 'specifications/list.html'
    permission_required = 'view_specifications'
    url_redirect = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [i.toLIST() for i in specifications.objects.select_related()]
                # for i in Category.objects.all():
                #     data.append(i.toJSON())
            elif action == 'delete':
                cat = specifications.objects.get(id=request.POST['id'])
                cat.delete()
            else:
                data['error'] = 'Ha ocurrido un error con el action'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de especificaciones'
        context['create_url'] = reverse_lazy('specifications_add')
        context['list_url'] = reverse_lazy('specifications_list')
        context['entity'] = 'Especificaciones'
        return context


class SpecificationsCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = specifications
    form_class = SpecificationsForm
    template_name = 'specifications/create.html'
    success_url = reverse_lazy('specifications_list')
    url_redirect = success_url
    permission_required = 'add_specifications'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    data['message'] = 'Especificación creada con éxito'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear especificaciones'
        context['entity'] = 'Especificaciones'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


# class CategoryUpdateView(ValidatePermissionRequiredMixin, UpdateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'category/create.html'
#     success_url = reverse_lazy('category_list')
#     url_redirect = success_url
#     permission_required = 'change_category'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'edit':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Edición una Categoria'
#         context['entity'] = 'Categorias'
#         context['list_url'] = self.success_url
#         context['action'] = 'edit'
#         return context


class QRcodeView(TemplateView):
    template_name = 'specifications/QRcode.html'

    # def get(self, request, *args, **kwargs):
    #     request.user.get_group_session()
    #     return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         data = {}
    #         now = datetime.now()
    #         action = request.POST['action']
    #         if action == 'search_investment':
    #             if request.user.is_superuser:
    #                 investment = Product.objects.select_related().aggregate(
    #                     result=Coalesce(Sum(F('stock') * F('cost')), 0.00, output_field=FloatField())).get('result')
    #                 pvp = Product.objects.all().aggregate(
    #                     result=Coalesce(Sum(F('stock') * F('pvp')), 0.00, output_field=FloatField())).get('result')
    #                 revenue = float(pvp) - float(investment)
    #                 data = [[1, f'{investment:.2f}', f'{revenue:.2f}']]
    #             else:
    #                 data['error'] = 'No tiene acceso a esta informacion'
    #         elif action == 'search_data':
    #             maximumProductSold = SaleProduct.objects.select_related().filter(sale__date_joined=now).values(
    #                 'product__name').annotate(
    #                 total=Sum(F('cant'))).order_by('-total')[:5]
    #             sold = []
    #             for x, maximumProductSold in enumerate(maximumProductSold):
    #                 sold.append([x + 1, maximumProductSold['product__name'], maximumProductSold['total']])
    #
    #             queryProducts = Product.objects.select_related()
    #             querySales = Sale.objects.select_related()
    #             if request.user.is_superuser:
    #                 sale = querySales.filter(date_joined__exact=now)
    #             else:
    #                 sale = querySales.filter(Q(user_id=request.user.id) & Q(date_joined__exact=now))
    #             lowInventory = queryProducts.filter(stock__lte=15).count()
    #             totalProductsQuery = queryProducts.count()
    #             totalClientsQuery = Client.objects.count()
    #             countSalesToday = sale.count()
    #             countSalesTodayMoney = sale.aggregate(
    #                 result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get('result')
    #             appliedCredit = querySales.filter(Q(payment='credit') & Q(applied=False)).count()
    #
    #             data = {
    #                 'sales-today': countSalesToday,
    #                 'sales': countSalesTodayMoney,
    #                 'products': totalProductsQuery,
    #                 'clients': totalClientsQuery,
    #                 'lower-inventory': lowInventory,
    #                 'maximumsold': sold,
    #                 'programing-clients': visitFrequency(request).count(),
    #                 'applied-credit': appliedCredit
    #             }
    #         elif action == 'search_presale_info':
    #             today = str(now.date())
    #             data = []
    #             exist = User.objects.filter(presale=True).exists()
    #             if exist:
    #                 query = visitFrequency(request)
    #                 cantProgramingCLients = query.filter(user__presale=True).values('user__username').annotate(
    #                     client=Count(F('id')))
    #                 cantSales = query.filter(Q(sale__date_joined=today) & Q(user__presale=True)).values(
    #                     'user__username').annotate(sale=Coalesce(Count('id'), 0))
    #
    #                 presales = [i.get('user__username') for i in cantSales]
    #
    #                 cpGeneral = 0  # Total clients programs today
    #                 ceGeneral = 0  # Total effectiveness clients
    #
    #                 for s in cantProgramingCLients:
    #                     if s['user__username'] in presales:
    #                         i = presales.index(s['user__username'])
    #                         sale = int(cantSales[i]['sale'])
    #                         effectiveness = (sale * 100) / s['client']
    #                         data.append([1, s['user__username'], s['client'],
    #                                      sale, effectiveness])
    #                         ceGeneral += sale
    #                     else:
    #                         effectiveness = (0 * 100) / s['client']
    #                         data.append([1, s['user__username'], s['client'],
    #                                      0, effectiveness])
    #                     cpGeneral += s['client']
    #
    #                 eGeneral = (ceGeneral * 100) / cpGeneral
    #                 data.append([1, '--------', cpGeneral, ceGeneral, eGeneral])
    #             else:
    #                 data = {'info': 'No hay pre ventas activos para calcular el reporte'}
    #                 return JsonResponse(data, safe=False)
    #         elif action == 'search_lower_inventory':
    #             queryProducts = Product.objects.filter(stock__lte=10)
    #             data = [p.toLIST() for p in queryProducts]
    #             # for p in queryProducts:
    #             #     data.append([p.id, p.name, p.brand.name, p.stock,
    #             #                  f'{p.cost:.2f}'])
    #         elif action == 'search_payment_method':
    #             data = []
    #             query = Sale.objects.select_related().filter(date_joined=now)
    #             cashPayment = query.filter(payment='cash')
    #             creditPayment = query.filter(payment='credit')
    #             posPayment = query.filter(payment='pos')
    #             transferPayment = query.filter(payment='trasnfer')
    #
    #             cash = cashPayment.aggregate(result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get(
    #                 'result')
    #             credit = creditPayment.aggregate(result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get(
    #                 'result')
    #             pos = posPayment.aggregate(result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get(
    #                 'result')
    #             transfer = transferPayment.aggregate(
    #                 result=Coalesce(Sum(F('total')), 0.00, output_field=FloatField())).get('result')
    #
    #             data.append(
    #                 [1, [cashPayment.count(), cash], [posPayment.count(), pos], [transferPayment.count(), transfer],
    #                  [creditPayment.count(), credit]])
    #             # data.append(
    #             #     [1, cashPayment.count(), posPayment.count(), transferPayment.count(), creditPayment.count()])
    #         elif action == 'get_graph_sales_year_month':
    #             points = []
    #             year = datetime.now().year
    #             for m in range(1, 13):
    #                 total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
    #                     result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
    #                 points.append(float(total))
    #             data = {
    #                 'name': 'Porcentaje de venta',
    #                 'showInLegend': False,
    #                 'colorByPoint': True,
    #                 'data': points
    #             }
    #         elif action == 'get_graph_sales_products_year_month':
    #             points = []
    #             year = datetime.now().year
    #             month = datetime.now().month
    #             for p in Product.objects.filter():
    #                 total = SaleProduct.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month,
    #                                                    product_id=p.id).aggregate(
    #                     result=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('result')
    #                 if total > 0:
    #                     points.append({'name': p.name, 'y': float(total)})
    #             data = {
    #                 'name': 'Porcentaje',
    #                 'colorByPoint': True,
    #                 'data': points
    #             }
    #         elif action == 'view-credit-noapplied':
    #             appliedCredit = Sale.objects.filter(Q(payment='credit') & Q(applied=False))
    #             data = []
    #             total = 0
    #             for i in appliedCredit:
    #                 total += i.total
    #                 data.append([i.id, i.purchase_order, i.user.username, i.client.names, i.end, i.total])
    #             data.append(['--', '----', '----', '----', 'Total', total])
    #     except Exception as e:
    #         print(str(e))
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)

    def get_information_view(self, id):
        for i in specifications.objects.select_related().filter(production_id=id):
            data = {
                'Lot number': i.production.id,
                'Product': i.production.detail_production_set.filter(product__category__name='PF'),
                'Production Date': i.production.date_joined.strftime('%d %b %Y'),
                'Characteristics': i.characteristics,
                'Chemical analysis': i.chemical_analysis,
                'Health certificate': i.get_file()
            }
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Specification Viewer'
        context['pk'] = self.kwargs['pk']
        context['query'] = self.get_information_view(self.kwargs['pk'])
        return context
