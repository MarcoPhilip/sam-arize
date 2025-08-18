from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory
from .forms import InventoryForm

User = get_user_model()

def home(request):
    return render(request, 'home.html') 

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# List inventory
def inventory_list(request):
    inventory = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventory': inventory})

# Add inventory
def inventory_add(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'inventory/inventory_add.html', {'form': form})

# Edit inventory
def inventory_edit(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory/inventory_list')
    else:
        form = InventoryForm(instance=item)
    return render(request, 'inventory_edit.html', {'form': form})

# Delete inventory
def inventory_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_delete_confirm.html', {'item': item})


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class SignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

