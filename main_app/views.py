from datetime import timedelta

# Auth Imports
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
# CBV Imports
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

# Form Imports
from .forms import InventoryForm, CategoryForm, LocationForm, SignupForm

# Models Imports
from .models import Inventory
from .forms import InventoryForm, CategoryForm, LocationForm, PurchaseOrderForm, AssetForm, SupplierForm
from .models import Category
from .models import Location
from .models import PurchaseOrder
from .models import Supplier
#
from django.shortcuts import render
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
import json


# Models Imports
from .models import Asset

User = get_user_model()
def purchase_order_list(request):
    orders = PurchaseOrder.objects.select_related("supplier").order_by("-order_date", "-id")
    return render(request, "purchase_order/purchase_order_list.html", {"orders": orders})

def purchase_order_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, "purchase_order/purchase_order_detail.html", {"order": order})

def purchase_order_create(request):
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("purchase_order_list")
    else:
        form = PurchaseOrderForm()
    return render(request, "purchase_order/purchase_order_form.html", {"form": form})

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

def purchase_order_delete(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("purchase_order_list")
    return render(request, "purchase_order/purchase_order_confirm_delete.html", {"order": order})

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


def home(request):
    return render(request, 'home.html') 

@login_required



#
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

# Asset List
@login_required
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
def inventory_detail(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    return render(request, "inventory/inventory_detail.html", {"inventory": inventory})

# Edit category
@login_required
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
def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_delete_confirm.html', {'item': item})

# Locations List
@login_required
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'location/location_list.html', {'locations': locations})

# Add a Location
@login_required
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
def location_detail(request, pk):
    locations = get_object_or_404(Location, pk=pk)
    return render(request, "location/location_detail.html", {"locations": locations})

# Edit a Location
@login_required
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
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location_list')
    return render(request, 'location/location_confirm_delete.html', {'location': location})

@login_required
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
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, "supplier/supplier_detail.html", {"supplier": supplier})

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
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        return redirect("supplier_list")
    return render(request, "supplier/supplier_confirm_delete.html", {"supplier": supplier})
 

class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset/asset_create.html"
    success_url = reverse_lazy("asset_index")

    # Set user as owner
    def form_valid(self, form):
        # ensure the owner is set to the logged-in user
        if not form.instance.owner_id:
            form.instance.owner = self.request.user
        return super().form_valid(form)

class AssetDetail(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = "asset/asset_detail.html"
    

class AssetUpdate(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset/asset_update.html"
    success_url = reverse_lazy("asset_index")

class AssetDelete(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = "asset/asset_confirm_delete.html"
    success_url = reverse_lazy("asset_index")
