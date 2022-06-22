from django.urls import path
from .views.provider.views import *
from .views.product.views import *
from .views.ingress.views import *
from .views.ctas_pay.views import *
from .views.inventory.views import *
from .views.category.views import *
from .views.banks.views import *

urlpatterns = [
    # banks
    path('banks/',BanksListView.as_view(), name='banks_list'),
    path('banks/add/', BanksCreateView.as_view(), name='banks_create'),
    path('banks/update/<int:pk>/', BanksUpdateView.as_view(), name='banks_update'),
    path('banks/delete/<int:pk>/', BanksDeleteView.as_view(), name='banks_delete'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # purchases
    path('purchases/', IngressListView.as_view(), name='ingress_list'),
    path('purchases/add/', IngressCreateView.as_view(), name='ingress_create'),
    path('purchases/delete/<int:pk>/', IngressDeleteView.as_view(), name='ingress_delete'),
    # ctas_pay
    path('ctas/pay/', CtasPayListView.as_view(), name='ctas_pay_list'),
    path('ctas/pay/delete/<int:pk>/', CtasPayDeleteView.as_view(), name='ctas_pay_delete'),
    # inventory
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
]
