from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import dashboard, home, SignupView, asset_index, AssetCreate, AssetUpdate, AssetDelete, AssetDetail

urlpatterns = [
    # Auth
    path('', home, name='home' ),
    path('login/',  LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    
    #purchase order
    
  
    path("purchase-order/", views.purchase_order_create, name="purchase_order"),
    path("purchase-list/", views.purchase_order_list, name="purchase_order_list"),
    path("purchase-orders/new/", views.purchase_order_create, name="purchase_order_create"),
    path("purchase-orders/<int:pk>/", views.purchase_order_detail, name="purchase_order_detail"),
    path("purchase-orders/<int:pk>/edit/", views.purchase_order_edit, name="purchase_order_edit"),
    path("purchase-orders/<int:pk>/delete/", views.purchase_order_delete, name="purchase_order_delete"),



    # dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Asset URLS
    path('assets/', asset_index, name='asset_index'),
    path('assets/new/', AssetCreate.as_view(), name="asset_create"),
    path('assets/<int:pk>', AssetDetail.as_view(), name="asset_detail"),
    path("assets/<int:pk>/edit", AssetUpdate.as_view(), name='asset_update'),
    path("assets/<int:pk>/delete", AssetDelete.as_view(), name='asset_delete'),

    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_add, name='inventory_add'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # Location URLs
    path('locations/', views.location_list, name='location_list'),
    path('locations/add/', views.location_add, name='location_add'),
    path('locations/<int:pk>/edit/', views.location_edit, name='location_edit'),
    path('locations/<int:pk>/delete/', views.location_delete, name='location_delete'),
    
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("suppliers/new/", views.supplier_create, name="supplier_create"),
    path("suppliers/<int:pk>/", views.supplier_detail, name="supplier_detail"),
    path("suppliers/<int:pk>/edit/", views.supplier_edit, name="supplier_edit"),
    path("suppliers/<int:pk>/delete/", views.supplier_delete, name="supplier_delete"),
]