from django.urls import path
from .views import CustomerApiView, CustomerDetailApiView, OrderApiView, HomeView, OrderDetailApiView

urlpatterns = [
  path('', HomeView.as_view(), name='home'),
  path('order/', OrderApiView.as_view(), name='order'),
  path('order/<int:pk>/', OrderDetailApiView.as_view(), name='order-detail'),
  path('customer/', CustomerApiView.as_view(), name='customer'),
  path('customer/<int:pk>/', CustomerDetailApiView.as_view(), name='customer-detail'),
]
