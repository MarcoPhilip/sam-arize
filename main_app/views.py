# Auth Imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# CBV Imports
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory
from .forms import InventoryForm, CategoryForm, LocationForm, AssetForm
from .models import Category
from .models import Location

# Models Imports
from .models import Asset

User = get_user_model()

def home(request):
    return render(request, 'home.html') 

@login_required
def dashboard(request):
    # TODO: pull real counts for cards
    return render(request, 'dashboard.html')

@login_required
def asset_index(request):
    assets = Asset.objects.all()
    return render(request, "asset/asset_list.html", {'assets': assets})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form, 'title': 'Add Category'})

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

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class SignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

class AssetCreate(CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset/asset_create.html"
    success_url = reverse_lazy("asset_index")

class AssetUpdate(UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset/asset_update.html"
    success_url = reverse_lazy("asset_index")

class AssetDelete(DeleteView):
    model = Asset
    template_name = "asset/asset_delete_confirm.html"
    success_url = reverse_lazy("asset_index")
