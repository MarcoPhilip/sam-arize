# Auth Imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# CBV Imports
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.shortcuts import render

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
    return render(request, "asset/index.html", {'assets': assets})



class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

class SignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

