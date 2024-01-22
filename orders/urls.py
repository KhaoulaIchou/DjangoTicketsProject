from django.urls import path
from . import views
from .views import OrderCreateView, OrderDeleteView, UserOrderListView


urlpatterns = [
    #path('orders/', views.orders, name='orders'),
    #path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    #path('orders/<int:order_id>/pay/', views.pay_order, name='pay_order'),
    path('order/new/<int:pk>/', OrderCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('myorders/', UserOrderListView.as_view(), name='user-orders'),
]
