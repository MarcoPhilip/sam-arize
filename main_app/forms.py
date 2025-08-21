from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Location, Inventory, PurchaseOrder, Supplier, Asset
from django.contrib.auth import get_user_model


AuthUser = get_user_model()

class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name  = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user
    
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'category', 'location', 'quantity', 'unit_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "category", "location", "serial_number", "purchase_date", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ["supplier", "order_date", "status"]
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "order_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_person", "phone_number", "email", "address"]
        widgets = {
           "name": forms.TextInput(attrs={"class": "form-control"}),
           "contact_person": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
