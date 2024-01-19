from django.urls import path

from core.pos.views.assets.views import *
from core.pos.views.brands.views import *
from core.pos.views.category.views import *
from core.pos.views.client.views import *
from core.pos.views.company.views import CompanyUpdateView
from core.pos.views.dashboard.views import *
from core.pos.views.load.views import loadCsvView
from core.pos.views.product.views import *
from core.pos.views.sale.views import *
from core.pos.views.shopping.views import *
from core.pos.views.supplier.view import *

urlpatterns = [
    # dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),

    # brand
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('brand/add/', BrandsCreateView.as_view(), name='brand_create'),
    path('brand/update/<int:pk>/', BrandsUpdateView.as_view(), name='brand_update'),

    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),

    # assets
    path('assets/', AssetsListView.as_view(), name='assets_list'),
    path('assets/add/', AssetsCreateView.as_view(), name='assets_create'),
    path('assets/update/<int:pk>/', AssetsUpdateView.as_view(), name='assets_update'),

    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),

    # supplier
    path('supplier/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/add', SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier/update/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update'),

    # shopping
    path('shopping/', ShoppingListView.as_view(), name='shopping_list'),
    path('shopping/add', ShoppingCreateView.as_view(), name='shopping_create'),
    path('shopping/update/<int:pk>/', ShoppingUpdateView.as_view(), name='shopping_update'),

    # sale
    path('sale/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    # path('sale/guides/', SaleInvoiceGuidesPdfView.as_view(), name='sale_guides_pdf'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),

    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),

    # load
    path('load/', loadCsvView.as_view(), name='load_csv'),

]
