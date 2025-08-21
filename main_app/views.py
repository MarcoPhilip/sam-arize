# Auth Imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# CBV Imports
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

# Form Imports
from .forms import InventoryForm, CategoryForm, LocationForm, SignupForm

# Models Imports
from .models import Inventory
from .models import Category
from .models import Location
from .models import Asset

User = get_user_model()

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
def dashboard(request):
    # TODO: pull real counts for cards
    return render(request, 'dashboard.html')

@login_required
def asset_index(request):
    assets = Asset.objects.all()
    return render(request, "asset/index.html", {'assets': assets})

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
def inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})

# Add inventory
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


class AssetCreate(CreateView):
    model = Asset
    fields = ["name", "category", "supplier", "cost", ]
