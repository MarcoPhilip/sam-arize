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
# Define the reports view function
def reports_view(request):
    # Render and return the "reports.html" template to the browser
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


# Asset List

@login_required
@groups_required("Manager", "Owner" ,"Staff")
def asset_index(request):
    assets = Asset.objects.all()
    return render(request, "asset/asset_list.html", {'assets': assets})

# List category
@login_required
# Define the function that will list all categories
def category_list(request):
    # Query the database to get all Category objects
    categories = Category.objects.all()
    # Render the category template
    # Pass the list of categories into the template as context
    return render(request, 'category/category_list.html', {'categories': categories})


# Detail for category
@login_required
# Define the function to display details of a single category
# It takes the request object and the primary key (pk) of the category
def category_detail(request, pk):
    # Fetch the category object with given pk form db
    category = get_object_or_404(Category, pk=pk)
    # render the category template
    return render(request, "category/category_detail.html", {"category": category})

# Add category
@login_required
# Authorization of groups
@groups_required("Manager", "Owner" ,"Staff")
# Define the function to add a new category
def category_add(request):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Bind the submitted POST data to the CategoryForm
        form = CategoryForm(request.POST)
        # Check if the form data is valid
        if form.is_valid():
            # Don't save yet just create an unsaved category
            category = form.save(commit=False)
            # Set the created by field and assign the logged-in user
            category.owner = request.user
            # Save to DB
            category.save()
            return redirect('category_list')
    # If the request is GET (or form is invalid), create an empty form
    else:
            form = CategoryForm()
    # Render the category form template
    return render(request, 'category/category_form.html', {'form': form, 'title': 'Add Category'})

# Inventory Details
@login_required
def inventory_detail(request, pk):
    # Fetch the inventory object with given pk form db
    inventory = get_object_or_404(Inventory, pk=pk)
    # Render the template
    return render(request, "inventory/inventory_detail.html", {"inventory": inventory})

# Edit category
@login_required
# Authorization of groups
@groups_required("Manager", "Owner")
def category_edit(request, pk):
    # Get the Category object with the given primary key (pk),
    category = get_object_or_404(Category, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the submitted POST data to the CategoryForm
        form = CategoryForm(request.POST, instance=category)
        # Validate the form data
        if form.is_valid():
            # Save the changes to DB
            form.save()
            # redirect back to category list
            return redirect('category_list')
    # If the request is not POST or form is invalid:
    else:
        # Create a form pre-filled with the existing category data
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, 'title': 'Edit Category'})

# Delete category
@login_required
# Authorization of groups
@groups_required("Owner")
def category_delete(request, pk):
    # Get the Category object with the given primary key (pk)
    category = get_object_or_404(Category, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the category from the database
        category.delete()
        # Redirect back to category list
        return redirect('category_list')
    # Render the template
    return render(request, 'category/category_confirm_delete.html', {'category': category})

# List inventory
@login_required
# Define a function to list all inventory items
def inventory_list(request):
    # Fetch all inventory objects from the database
    inventories = Inventory.objects.all()
    # Render the template
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})

# Add inventory
@login_required
# Authorization of groups
@groups_required("Manager", "Owner" ,"Staff")
# Define a function to add inventory items

def inventory_add(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the submitted POST data to the InventoryForm
        form = InventoryForm(request.POST)
        if form.is_valid():
            # Don't save yet 
            inventory = form.save(commit=False)
            # Set the created by field and assign to logged in user
            inventory.owner = request.user
            # Now save to DB
            inventory.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Add Inventory'})

# Edit inventory
@login_required
# Authorization of groups
@groups_required("Manager", "Owner")
def inventory_edit(request, pk):
    # Get the inventory object with the given primary key
    inventory = get_object_or_404(Inventory, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the submitted POST data
        form = InventoryForm(request.POST, instance=inventory)
        # Validate the form data
        if form.is_valid():
            # Save the changes to DB
            form.save()
            # redirect back to inventory list
            return redirect('inventory_list')
       # If the request is not POST or form is invalid:
    else:
        # Create a form pre-filled with the existing inventory data
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'title': 'Edit Inventory'})

# Delete inventory
@login_required
# Authorization of groups
@groups_required("Owner")
def inventory_delete(request, pk):
    # Get the inventory object with the given primary key (pk)
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        # Delete from DB
        item.delete()
        # Redirect back to inventory list
        return redirect('inventory_list')
    # Render the template
    return render(request, 'inventory/inventory_delete_confirm.html', {'item': item})

def inventory_report(request, period):
    # Get today's date
    today = timezone.now().date()
    # Check what period was requested
    if period == "week":
        # For weekly report: include items from the last 7 days
        start_date = today - timedelta(days=7)
    elif period == "month":
        # For monthly report: include items from the start of the current month
        start_date = today.replace(day=1)
    elif period == "year":
        # For yearly report: include items from the start of the current year
        start_date = today.replace(month=1, day=1)
    else:
        # If an invalid period is passed, fallback to today's date only
        start_date = today
     # Fetch inventory records created after the start_date
    inventories = Inventory.objects.filter(created_at__gte=start_date)

    return render(request, "inventory/report.html", {
        "inventories": inventories,
        "period": period.capitalize()
    })

# Locations List
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def location_list(request):
    # Fetch all location objects from the database
    locations = Location.objects.all()
    # Render the template
    return render(request, 'location/location_list.html', {'locations': locations})

# Add a Location
@login_required
@groups_required("Manager", "Owner")
def location_add(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the submitted POST data
        form = LocationForm(request.POST)
        if form.is_valid():
            # Don't save yet just create an unsaved location
            location = form.save(commit=False)
            # Set the created_by field and assing the logged in user
            location.owner = request.user
            # Save to DB 
            location.save()
            # Redirect to location list
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'location/location_form.html', {'form': form, 'title': 'Add Location'})

# Location detail
@login_required
@groups_required("Manager", "Owner" ,"Staff")
def location_detail(request, pk):
    # Fetch all location objects from the database
    locations = get_object_or_404(Location, pk=pk)
    # Render the template
    return render(request, "location/location_detail.html", {"locations": locations})

# Edit a Location
@login_required
@groups_required("Manager", "Owner")
def location_edit(request, pk):
    # Get the location object with the given primary key (pk),
    location = get_object_or_404(Location, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the submitted POST data
        form = LocationForm(request.POST, instance=location)
        # Validate the form data
        if form.is_valid():
            # Save changes to DB
            form.save()
            # Return to location list
            return redirect('location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'location/location_form.html', {'form': form, 'title': 'Edit Location'})

# Delete a Location
@login_required
@groups_required("Owner")
def location_delete(request, pk):
    # Get the location object with the given primary key (pk),
    location = get_object_or_404(Location, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete from DB
        location.delete()
        # Return to location list
        return redirect('location_list')
    # Render the template
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
        # check if user is authenticated 
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

    # Set user as owner
    def form_valid(self, form):
        # ensure the owner is set to the logged-in user
        if not form.instance.owner_id:
            form.instance.owner = self.request.user
        return super().form_valid(form)
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
