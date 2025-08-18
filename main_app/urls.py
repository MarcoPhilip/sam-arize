from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import dashboard, home, SignupView
from . import views

urlpatterns = [
    # Auth
    path('', home, name='home' ),
    path('login/',  LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_add, name='inventory_add'),
    path('inventory/edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('inventory/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    # Example dashboard (protected)

    # TODO: Dashboard route needs to be protected. Home page('') route isnt protected. If logged in, send the user to dashboard. Else, send to home. 
    path('dashboard/', dashboard, name='dashboard'),
]