import csv
import json
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q, Sum, F
from django.http import HttpResponse, FileResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DeleteView, UpdateView, View
import os

from core.pos.choices import personalized_invoice
from core.pos.mergerPdfFiles import mergerPdf
from core.user.models import User

# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
from weasyprint import HTML, CSS

from core.pos.forms import SaleForm, ClientForm, SaleMovilForm
from core.pos.mixins import ValidatePermissionRequiredMixin, ExistsCompanyMixin, deviceVerificationMixin
from core.pos.models import Sale, Product, SaleProduct, Client, Company
from core.reports.forms import ReportForm


class SaleListView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    def guide(self, param: dict):
        data = {}
        try:
            dirname = os.path.join(settings.MEDIA_ROOT, 'merger')
            directorySchema = os.path.join(dirname, param['tenant'])
            if not os.path.isdir(directorySchema):
                os.mkdir(directorySchema)
            now = datetime.now()
            user = param['user']
            today = str(now.date())
            hour = f'{now.hour}:{now.minute}'
            # today = '2023-09-08'
            id = int(param['id'])

            query = Sale.objects.select_related().filter(Q(date_joined=today) & Q(user__presale=True))
            querySales = query.filter(Q(user_id=id) & Q(endofday__exact=False))
            # COLLECT ALL THE SALES FOR ESPESIFIC USER
            detailProducts = querySales.order_by('-saleproduct__product__category_id').values(
                'saleproduct__product__category__name', 'saleproduct__product__code', 'saleproduct__product__name',
                'saleproduct__price').annotate(cant=Sum('saleproduct__cant')).annotate(
                subtotal=Sum('saleproduct__subtotal'))

            if detailProducts.count() != 0:
                # CALCULATE INVOICE
                iva = querySales.aggregate(result=Sum(F('total_iva'))).get('result')
                subtotal = 0.00
                totalProducts = 0
                for det in detailProducts:
                    subtotal += float(det['subtotal'])
                    totalProducts += det['cant']
                totalInvoice = subtotal + float(iva)
                calculate = {'subtotal': subtotal, 'iva': 0.15, 'total_iva': float(iva), 'total': totalInvoice,
                             'all_product': totalProducts}

                # CREATE A PDF FOR THE GUIDE TO DAY
                template = get_template('sale/guide.html')
                context = {
                    'user': user,
                    'products': detailProducts,
                    'calculate': calculate,
                    'company': Company.objects.first(),
                    'today': today,
                    'hour': hour,
                    'icon': f'{settings.MEDIA_URL}logo.png'
                }
                html = template.render(context)
                css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
                pdfGruide = HTML(string=html, base_url=param['uri']).write_pdf(
                    stylesheets=[CSS(css_url)])
                f = open(os.path.join(directorySchema, 'guide.pdf'), 'wb')
                f.write(pdfGruide)
                f.close()

                # CREATE A PDFS FOR ALL SALES TODAY
                for q in querySales:
                    q.end_day()

                template = get_template('sale/invoice2.html')
                context = {
                    'query': querySales,
                    'today': today,
                    'icon': f'{settings.MEDIA_URL}logo.png'
                }
                html = template.render(context)
                css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
                pdfInvoice = HTML(string=html, base_url=param['uri']).write_pdf(
                    stylesheets=[CSS(css_url)])
                f = open(os.path.join(directorySchema, 'invoices.pdf'), 'wb')
                f.write(pdfInvoice)
                f.close()
                pd = mergerPdf(directorySchema, param['tenant'])
                # return HttpResponse(pd['path'], content_type='application/pdf')
                data['path'] = pd['path']
                return data
            else:
                data['info'] = 'No se encontraron ventas registradas del preventa'
                return data
        except  Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'apply_credit':
                s = Sale.objects.get(id=request.POST['id'])
                s.applied = True
                s.save()
            elif action == 'download_guides':
                data = []
                param = {
                    'id': request.POST['id'],
                    'tenant': request.tenant.schema_name,
                    'user': request.user,
                    'uri': request.build_absolute_uri()
                }
                path = self.guide(param)
                data = path
            elif action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.select_related()
                if len(start_date) and len(end_date) and request.user.is_superuser:
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                elif len(start_date) and len(end_date) and not request.user.is_superuser:
                    queryset = queryset.filter(
                        Q(user_id=request.user.id) & Q(date_joined__range=[start_date, end_date]))
                elif not len(start_date) and not len(end_date) and not request.user.is_superuser:
                    queryset = queryset.filter(user_id=request.user.id)

                for i in queryset:
                    data.append(i.toLIST())
            elif action == 'search_products_detail':
                data = []
                for i in SaleProduct.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'delete':
                sale = Sale.objects.get(id=request.POST['id'])
                set = sale.saleproduct_set.all()
                for s in set:
                    s.product.stock += s.cant
                    s.save()
                sale.delete()
            else:
                data['error'] = 'No se ha encontrado el acttion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('sale_create')
        context['list_url'] = reverse_lazy('sale_list')
        context['entity'] = 'Ventas'
        context['pre_sales'] = User.objects.filter(presale=True)
        return context


class SaleCreateView(deviceVerificationMixin, ExistsCompanyMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    # form_class = ''
    # template_name = ''
    success_url = reverse_lazy('sale_list')
    url_redirect = success_url
    permission_required = 'add_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(Q(stock__gt=0) | Q(is_inventoried=False))
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                # products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                products = Product.objects.filter(Q(name__icontains=term) | Q(code__icontains=term)).filter(
                    Q(stock__gt=0) | Q(is_inventoried=False))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    now = datetime.now()
                    today = str(now.date())
                    exist = Sale.objects.filter(Q(date_joined=today) & Q(client_id=request.POST['client'])).exists()
                    if exist:
                        data['error'] = 'El cliente ya cuenta con una factura, favor de modificar la actual'
                    else:
                        sale = Sale()
                        sale.user_id = request.user.id
                        sale.date_joined = request.POST['date_joined']
                        sale.purchase_order = request.POST['purchase_order']
                        sale.client_id = int(request.POST['client'])
                        if request.POST['payment'] == 'credit':
                            sale.payment = request.POST['payment']
                            sale.days = request.POST['days']
                            sale.end = request.POST['end']
                        else:
                            sale.payment = request.POST['payment']
                        sale.iva = float(request.POST['iva'])
                        sale.save()
                        for i in products:
                            detail = SaleProduct()
                            detail.sale_id = sale.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])
                            detail.price = float(i['pvp'])
                            detail.subtotal = detail.cant * detail.price
                            detail.save()
                            if detail.product.is_inventoried:
                                detail.product.stock -= detail.cant
                                detail.product.save()

                        sale.calculate_invoice()
                        data = {'id': sale.id}
            elif action == 'search_if_exits_client':
                now = datetime.now()
                today = str(now.date())
                exists = Sale.objects.filter(Q(date_joined=today) & Q(client_id=request.POST['id_client'])).exists()
                if exists:
                    data['exists'] = True
                    data['success_url'] = self.success_url
                else:
                    data['exists'] = False
            elif action == 'search_client':
                data = []
                today = datetime.today().strftime('%A')[:3].lower()
                if request.user.is_superuser:
                    query = Client.objects.select_related().filter(is_active=True)
                else:
                    query = Client.objects.select_related().filter(Q(is_active=True) & Q(user_id=request.user.id))

                if today == 'mon':
                    queryFilter = query.filter(Q(frequent=True) | Q(mon=True))
                elif today == 'tue':
                    queryFilter = query.filter(Q(frequent=True) | Q(tue=True))
                elif today == 'wed':
                    queryFilter = query.filter(Q(frequent=True) | Q(wed=True))
                elif today == 'thu':
                    queryFilter = query.filter(Q(frequent=True) | Q(thu=True))
                elif today == 'fri':
                    queryFilter = query.filter(Q(frequent=True) | Q(fri=True))
                elif today == 'sat':
                    queryFilter = query.filter(Q(frequent=True) | Q(sat=True))
                else:
                    queryFilter = query

                term = request.POST['term']
                clients = queryFilter.filter(
                    Q(names__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    form = ClientForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        id = self.request.user.id
        form = ClientForm(initial={'user': User.objects.get(id=id)})
        # form.fields['user'].widget.attrs['hidden'] = True
        context['frmClient'] = form
        return context


class SaleUpdateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    # form_class = ''
    # template_name = ''
    success_url = reverse_lazy('sale_list')
    url_redirect = success_url
    permission_required = 'change_sale'

    def get_form(self, form_class=None):
        module = self.request.path.split('/')[3]
        if module == 'update':
            instance = self.get_object()
            if 'Sec-Ch-Ua-Mobile' in self.request.headers:
                if self.request.headers['Sec-Ch-Ua-Mobile'] == '?1':
                    form = SaleMovilForm(instance=instance)
                    form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
                    self.template_name = 'sale/createmovil2.html'
                elif self.request.headers['Sec-Ch-Ua-Mobile'] == '?0':
                    form = SaleForm(instance=instance)
                    form.fields['client'].queryset = Client.objects.filter(id=instance.client.id)
                    self.template_name = 'sale/create.html'
                return form

    def get_details_product(self):
        data = []
        sale = self.get_object()
        print(sale)
        for i in sale.saleproduct_set.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        print(data)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(Q(stock__gt=0) | Q(is_inventoried=False))
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term).filter(Q(stock__gt=0) | Q(is_inventoried=False))
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    products_review = json.loads(request.POST['products_review'])

                    sale = self.get_object()
                    sale.date_joined = request.POST['date_joined']
                    sale.client_id = int(request.POST['client'])
                    if request.POST['payment'] == 'credit':
                        sale.payment = request.POST['payment']
                        sale.days = request.POST['days']
                        sale.end = request.POST['end']
                    else:
                        sale.payment = request.POST['payment']
                    sale.iva = float(request.POST['iva'])
                    sale.save()

                    sale.saleproduct_set.all().delete()
                    listProductId = []  # Lista que obtendra los id de los productos ingresados
                    pr = [pr.get('id') for pr in products_review]

                    for p in products:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = int(p['id'])
                        detail.cant = int(p['cant'])
                        detail.price = float(p['pvp'])
                        detail.subtotal = detail.cant * detail.price
                        detail.save()
                        if detail.product.is_inventoried:
                            if p['id'] in pr:
                                indice = pr.index(p['id'])
                                # print('indice existe: ', indice)
                                detail.product.stock = (detail.product.stock + products_review[indice]['cant']) - \
                                                       p['cant']
                                detail.product.cost = float(p['cost'])
                                detail.product.pvp = float(p['pvp'])
                                detail.product.save()
                            else:
                                detail.product.stock -= p['cant']
                                detail.product.cost = float(p['cost'])
                                detail.product.pvp = float(p['pvp'])
                                detail.product.save()
                        listProductId.append(p['id'])

                    if len(pr) != 0:
                        for i in pr:
                            if i not in listProductId:
                                indice = pr.index(i)
                                # print('indice no existe: ', indice)
                                # print('No existe: ', i)
                                detail.product_id = int(i)
                                detail.product.stock = detail.product.stock + products_review[indice]['cant']
                                detail.product.cost = float(products_review[indice]['cost'])
                                detail.product.pvp = float(products_review[indice]['pvp'])
                                detail.product.save()

                    sale.calculate_invoice()
                    data = {'id': sale.id}
                data = {'id': sale.id}
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    form = ClientForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        context['frmClient'] = ClientForm()
        return context


class SaleInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            tenantName = 'disam'
            # tenantName = request.tenant.name
            templateName = tenantName + '.html'

            sale = Sale.objects.get(pk=self.kwargs['pk'])

            if tenantName in personalized_invoice:
                template = get_template('sale/' + templateName)
                saleLines = sale.saleproduct_set.all().count()
                lines = personalized_invoice[tenantName]
                jump = (lines - saleLines) + 1
                print(jump)
                listJump = [i for i in range(jump)]
            else:
                template = get_template('sale/invoice.html')
                listJump = []
            context = {
                'sale': sale,
                'icon': f'{settings.MEDIA_URL}logo.png',
                'jump': listJump,
            }

            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('sale_list'))

# class SaleInvoiceGuidesPdfView(LoginRequiredMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         try:
#             print(request.POST['id'])
#             data = {}
#             dirname = os.path.join(settings.MEDIA_ROOT, 'merger')
#             directorySchema = os.path.join(dirname, request.tenant.schema_name)
#             if not os.path.isdir(directorySchema):
#                 os.mkdir(directorySchema)
#             now = datetime.now()
#             user = request.user
#             today = str(now.date())
#             hour = f'{now.hour} : {now.minute}'
#             # today = '2023-09-08'
#             id = request.POST['id']
#
#             if id == 0:
#                 # COLLECT ALL THE SALES OF THE DAY
#                 detailProducts = SaleProduct.objects.filter(Q(sale__date_joined=today) & Q(endofday__exact=False)) \
#                     .values('product__name', 'price').annotate(cant=Sum('cant')).annotate(subtotal=Sum('subtotal'))
#             else:
#                 # COLLECT ALL THE SALES FOR ESPESIFIC USER
#                 detailProducts = SaleProduct.objects.filter(
#                     Q(sale__date_joined=today) & Q(sale__user_id=id) & Q(endofday__exact=False)) \
#                     .values('product__name', 'price').annotate(cant=Sum('cant')).annotate(subtotal=Sum('subtotal'))
#
#             print(detailProducts)
#             if detailProducts.count() != 0:
#                 # CALCULATE INVOICE
#                 subtotal = 0.00
#                 totalProducts = 0
#                 for det in detailProducts:
#                     subtotal += float(det['subtotal'])
#                     totalProducts += det['cant']
#                 ivaCalculado = subtotal * 0.15
#                 totalInvoice = subtotal + ivaCalculado
#                 calculate = {'subtotal': subtotal, 'iva': 0.15, 'total_iva': ivaCalculado, 'total': totalInvoice,
#                              'all_product': totalProducts}
#
#                 # CREATE A PDF FOR THE GUIDE TO DAY
#                 template = get_template('sale/guide.html')
#                 context = {
#                     'user': user,
#                     'products': detailProducts,
#                     'calculate': calculate,
#                     'company': Company.objects.first(),
#                     'today': today,
#                     'hour': hour,
#                     'icon': f'{settings.MEDIA_URL}logo.png'
#                 }
#                 html = template.render(context)
#                 css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
#                 pdfGruide = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
#                     stylesheets=[CSS(css_url)])
#                 f = open(os.path.join(directorySchema, 'guide.pdf'), 'wb')
#                 f.write(pdfGruide)
#                 f.close()
#
#                 # CREATE A PDFS FOR ALL SALES TO DAY
#                 if id == 0:
#                     # COLLECT ALL THE SALES OF THE DAY
#                     query = Sale.objects.filter(
#                         Q(date_joined=today) & Q(user__presale=True) & Q(saleproduct__endofday=False))
#                 else:
#                     query = Sale.objects.filter(
#                         Q(date_joined=today) & Q(user_id=id) & Q(saleproduct__endofday=False))
#
#                 for q in query:
#                     s = q.saleproduct_set.all()
#                     for i in s:
#                         i.end_day()
#
#                 template = get_template('sale/invoice2.html')
#                 context = {
#                     'query': query,
#                     'today': today,
#                     'icon': f'{settings.MEDIA_URL}logo.png'
#                 }
#                 html = template.render(context)
#                 css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
#                 pdfInvoice = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
#                     stylesheets=[CSS(css_url)])
#                 f = open(os.path.join(directorySchema, 'invoices.pdf'), 'wb')
#                 f.write(pdfInvoice)
#                 f.close()
#                 pd = mergerPdf(directorySchema, request.tenant.schema_name)
#                 # return HttpResponse(pd['path'], content_type='application/pdf')
#                 return JsonResponse(pd['path'], safe=False)
#             data['info'] = 'No se encontraron ventas de hoy'
#             return JsonResponse(data, safe=False)
#         except:
#             pass
#         return HttpResponseRedirect(reverse_lazy('sale_list'))
