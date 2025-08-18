from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, SignupView
from . import views

urlpatterns = [
    # Auth
    path('login/',  LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    # Example dashboard (protected)
    path('', dashboard, name='dashboard'),
    
    #purchase order
    
    urlpatterns = [
    path("purchase-order/", views.purchase_order_create, name="purchase_order"),
    path("purchase-orders/", views.purchase_order_list, name="purchase_order_list"),
]
]