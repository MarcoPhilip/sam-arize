from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import dashboard, home, SignupView

urlpatterns = [
    # Auth
    path('', home, name='home' ),
    path('login/',  LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
  
    # Example dashboard (protected)
    path('', dashboard, name='dashboard'),
    
    #purchase order
    
  
    path("purchase-order/", views.purchase_order_create, name="purchase_order"),
    path("purchase-orders/", views.purchase_order_list, name="purchase_order_list"),

    # TODO: Dashboard route needs to be protected. Home page('') route isnt protected. If logged in, send the user to dashboard. Else, send to home. 
    path('dashboard/', dashboard, name='dashboard'),
]