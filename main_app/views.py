from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta

# Auth Imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

# CBV Imports
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

# Form Imports
from .forms import InventoryForm, CategoryForm, LocationForm, PurchaseOrderForm, AssetForm, SupplierForm, SignupForm

# Models Imports
from .models import Inventory
from .models import Category
from .models import Location
from .models import PurchaseOrder
from .models import Supplier
from .models import Asset

User = get_user_model()


# Group Permisions
def groups_required(*group_names):

    # Define a nested function that will wrap the original view function
    def decorator(view_func):

        # Preserve the original view function’s metadata (name, docstring)
        @wraps(view_func)

        # Define the function that will actually run when the view is called
        # Accepts the same arguments as the original view
        def _wrapped_view(request, *args, **kwargs):

            # ✅ Superuser bypasses group checks
            if request.user.is_authenticated and request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if the user is logged in AND belongs to any of the allowed groups
            if request.user.is_authenticated and request.user.groups.filter(name__in=group_names).exists():
                # If the user is authorized, call the original view with the same arguments
                return view_func(request, *args, **kwargs)
            
            # If the user is not authorized, return a 403 Forbidden response with a message
            return HttpResponseForbidden("You are not authorized to access this page.")

        return _wrapped_view

    return decorator


# Home page
def home(request):
    return render(request, 'home.html') 

# View reports
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def reports_view(request):
    return render(request, "reports.html")

# View purchase order list
@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.select_related("supplier").order_by("-order_date", "-id")
    return render(request, "purchase_order/purchase_order_list.html", {"orders": orders})

# Detail of purchase order
@login_required
def purchase_order_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, "purchase_order/purchase_order_detail.html", {"order": order})

# Add purchase order
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def purchase_order_create(request):
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("purchase_order_list")
    else:
        form = PurchaseOrderForm()
    return render(request, "purchase_order/purchase_order_form.html", {"form": form})

# Edit purchase order
@login_required
@groups_required("Manager", "Owner")
def purchase_order_edit(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("purchase_order_detail", pk=order.pk)
    else:
        form = PurchaseOrderForm(instance=order)
    return render(request, "purchase_order/purchase_order_form.html", {"form": form})

# Delete purchase order
@login_required
@groups_required("Owner")
def purchase_order_delete(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("purchase_order_list")
    return render(request, "purchase_order/purchase_order_confirm_delete.html", {"order": order})

# Sign up 
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Staff'
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
@groups_required("Manager", "Owner" ,"Staff")
def dashboard(request):
    # KPIs
    kpi = {
        "assets": Asset.objects.count(),
        "suppliers": Supplier.objects.count(),
        "pos_open": PurchaseOrder.objects.filter(status__in=["pending","confirmed"]).count(),
        "pos_delivered": PurchaseOrder.objects.filter(status="delivered").count(),
    }
    # Tables
    recent_pos = PurchaseOrder.objects.select_related("supplier").order_by("-order_date", "-id")[:5]
    low_stock  = Inventory.objects.order_by("quantity")[:5] 

    context = {
        "kpi": kpi,
        "recent_pos": recent_pos,
        "low_stock": low_stock,


    }
    return render(request, "dashboard.html", context)


@login_required
@groups_required("Manager", "Owner" ,"Staff")
def asset_index(request):
    assets = Asset.objects.all()
    return render(request, "asset/asset_list.html", {'assets': assets})


# List category
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


# Detail for category
@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, "category/category_detail.html", {"category": category})

# Add category
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Don't save yet
            category = form.save(commit=False)
            # Set the created_by field
            category.created_by = request.user
            # Now save to DB
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def inventory_detail(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    return render(request, "inventory/inventory_detail.html", {"inventory": inventory})

# Edit category
@login_required
@groups_required("Manager", "Owner")
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, 'title': 'Edit Category'})

# Delete category
@login_required
@groups_required("Owner")
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category})

# List inventory
@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})

# Add inventory
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def inventory_add(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Edit Inventory'})

# Edit inventory
@login_required
@groups_required("Manager", "Owner")
def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Edit Inventory'})

# Delete inventory
@login_required
@groups_required("Owner")
def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_delete_confirm.html', {'item': item})

def inventory_report(request, period):
    today = timezone.now().date()

    if period == "week":
        start_date = today - timedelta(days=7)
    elif period == "month":
        start_date = today.replace(day=1)
    elif period == "year":
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today  # fallback

    inventories = Inventory.objects.filter(created_at__gte=start_date)

    return render(request, "inventory/report.html", {
        "inventories": inventories,
        "period": period.capitalize()
    })

# Locations List
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'location/location_list.html', {'locations': locations})

# Add a Location
@login_required
@groups_required("Manager", "Owner")
def location_add(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'location/location_form.html', {'form': form, 'title': 'Add Location'})

# Location detail
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def location_detail(request, pk):
    locations = get_object_or_404(Location, pk=pk)
    return render(request, "location/location_detail.html", {"locations": locations})

# Edit a Location
@login_required
@groups_required("Manager", "Owner")
def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'location/location_form.html', {'form': form, 'title': 'Edit Location'})

# Delete a Location
@login_required
@groups_required("Owner")
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location_list')
    return render(request, 'location/location_confirm_delete.html', {'location': location})

@login_required
@groups_required("Manager", "Owner" ,"Staff")
def supplier_list(request):
    query = request.GET.get('q')
    if query:
        suppliers = Supplier.objects.filter(
            name__icontains=query
        ) | Supplier.objects.filter(
            contact_person__icontains=query
        ) | Supplier.objects.filter(
            email__icontains=query
        )
    else:
        supplier = Supplier.objects.all()
    
    return render(request, 'supplier/supplier_list.html', {'supplier': supplier})

@login_required
@groups_required("Manager", "Owner")
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, "supplier/supplier_detail.html", {"supplier": supplier})


@login_required
@groups_required("Manager", "Owner")
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SupplierForm()
    return render(request, "supplier/supplier_form.html", {"form": form, "mode": "create"})

@login_required
@groups_required("Manager", "Owner")
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("supplier_detail", pk=supplier.pk)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, "supplier/supplier_form.html", {"form": form, "mode": "edit", "supplier": supplier})

@login_required
@groups_required("Owner")
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        return redirect("supplier_list")
    return render(request, "supplier/supplier_confirm_delete.html", {"supplier": supplier})
 


class GroupRequiredMixin:
    groups_required = None

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            # Superuser always allowed
            if user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            
            # Groups specified
            if self.groups_required and user.groups.filter(name__in=self.groups_required).exists():
                return super().dispatch(request, *args, **kwargs)

        # If none matched
        messages.error(request, "You are not authorized to access this feature.")
        return HttpResponseForbidden("You are not authorized to access this feature.")

class AssetCreate(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset/asset_create.html"
    groups_required = ["Manager", "Owner", "Staff"]
    success_url = reverse_lazy("asset_index")

class AssetDetail(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Asset
    template_name = "asset/asset_detail.html"
    groups_required = ["Manager", "Owner", "Staff"]
    

class AssetUpdate(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset/asset_update.html"
    groups_required = ["Manager", "Owner", ]
    success_url = reverse_lazy("asset_index")

class AssetDelete(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Asset
    template_name = "asset/asset_confirm_delete.html"
    groups_required = ["Owner"]
    success_url = reverse_lazy("asset_index")
