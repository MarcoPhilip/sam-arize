from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import dashboard, home, SignupView, asset_index, AssetCreate

urlpatterns = [
    # Auth
    path('', home, name='home' ),
    path('login/',  LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
  
    # Example dashboard (protected)

    # TODO: Dashboard route needs to be protected. Home page('') route isnt protected. If logged in, send the user to dashboard. Else, send to home. 
    path('dashboard/', dashboard, name='dashboard'),
    path('assets/', asset_index, name='asset_index'),
    path('assets/new/', AssetCreate.as_view(), name="asset_create")
]