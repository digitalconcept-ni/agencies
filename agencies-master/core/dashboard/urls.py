from django.urls import path

from core.pos.views.assets.views import *
from core.pos.views.brands.views import *
from core.pos.views.category.views import *
from core.pos.views.client.views import *
from core.pos.views.company.views import CompanyUpdateView
from core.dashboard.views import *
from core.pos.views.load.views import loadCsvView
from core.pos.views.loss.view import *
from core.pos.views.product.views import *
from core.pos.views.sale.views import *
from core.pos.views.shopping.views import *
from core.pos.views.supplier.view import *

urlpatterns = [
    # dashboard
    path('', DashboardView.as_view(), name='dashboard'),
]
