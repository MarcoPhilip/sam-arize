from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect  
from django.utils import timezone
from django.db.models import Sum, F

from .models import PurchaseOrder


User = get_user_model()

def home(request):
    return render(request, 'home.html') 

@login_required
def dashboard(request):
    # Public / user dashboard (leave as-is or fill with user-facing stats)
    return render(request, 'dashboard.html')


# STAFF-ONLY ADMIN DASHBOARD
@staff_member_required
def admin_dashboard(request):
    """
    Staff-only dashboard with totals and recent activity.
    Make sure your user has is_staff=True (via /admin).
    """
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)


    total_pos = PurchaseOrder.objects.count()
    total_value = PurchaseOrder.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    # Last 7 days
    pos_last_7 = PurchaseOrder.objects.filter(created_at__date__gte=week_ago).count()
    value_last_7 = PurchaseOrder.objects.filter(created_at__date__gte=week_ago).aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    recent_pos = PurchaseOrder.objects.order_by('-created_at')[:5]

    context = {
        "cards": [

            {"label": "Purchase Orders", "value": total_pos},
            {"label": "Total PO Value ($)", "value": f"{total_value:,.2f}"},
        ],
        "pos_last_7": pos_last_7,
        "value_last_7": f"{value_last_7:,.2f}",
        "recent_pos": recent_pos,
        "today": today,
        "week_ago": week_ago,
    }
    return render(request, 'admin_dashboard.html', context)
# /STAFF-ONLY ADMIN DASHBOARD


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class SignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")


def purchase_order_create(request):
    if request.method == "POST":
        supplier = request.POST.get("supplier")
        item = request.POST.get("item")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")

        PurchaseOrder.objects.create(
            supplier=supplier,
            item=item,
            quantity=quantity,
            price=price
        )
        return redirect("purchase_order_list")

    return render(request, "inventory/purchase_order.html")


def purchase_order_list(request):
    orders = PurchaseOrder.objects.all().order_by("-created_at")
    return render(request, "inventory/purchase_order_list.html", {"orders": orders})