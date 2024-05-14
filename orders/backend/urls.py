from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

router = DefaultRouter()
router.register('suppliers/', SupplierSerializerViewSet)

urlpatterns = [
    path('user/register/', RegisterUser.as_view(), name='register'),
    path('user/login/', LoginUser.as_view(), name='login'),
    path('supplier_product/', SupplierProductInfoView.as_view(), name='supplier_product'),
    path('supplier_product/<int:id>/', SupplierProductInfoView.as_view()),
    path('products_info/', ProductInfoView.as_view(), name='products_info'),
    path('order_item/', OrderItemCreateView.as_view(), name='order_item_create'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('user/contact', ContactView.as_view(), name='user_contact'),
    path('user/contact/<int:id>/', ContactView.as_view(), name='user_contact'),
    path('order/', OrderItemListView.as_view(), name='order'),
    path('dowload_data/', views.dowload_add_info, name='dowload_data')
]

urlpatterns += router.urls
