from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder

import json

from .models import Component, Build, Order, Profile
from pcbuilderlib import calculate_price


def home(request):
    return render(request, "home.html")


def pc_builder(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    sector = request.GET.get("sector", "Gaming")
    edit_id = request.GET.get("edit")

    components = Component.objects.filter(sector=sector)

    existing_build_data = None

    if edit_id and request.user.is_authenticated:
        saved_build = Build.objects.filter(id=edit_id, user=request.user).first()

        if saved_build:
            existing_build_data = {}

            component_types = [
                "cpu", "gpu", "ram", "storage",
                "motherboard", "psu", "case", "cooling"
            ]

            for comp_type in component_types:
                comp_name = getattr(saved_build, comp_type)

                if comp_name:
                    component = Component.objects.filter(
                        name=comp_name,
                        category=comp_type,
                        sector=saved_build.sector
                    ).first()

                    if component:
                        existing_build_data[comp_type] = {
                            "name": component.name,
                            "price": component.price,
                            "socket": component.socket,
                            "ram_type": component.ram_type,
                            "power": component.power
                        }

    context = {
        "sector": sector,
        "components": components,
        "existing_build_data_json": json.dumps(existing_build_data, cls=DjangoJSONEncoder)
    }

    return render(request, "builder.html", context)


@login_required
def save_build(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    sector = request.GET.get("sector", "Gaming")

    components = [
        data.get("cpu", {}),
        data.get("gpu", {}),
        data.get("ram", {}),
        data.get("motherboard", {}),
        data.get("storage", {}),
        data.get("psu", {}),
        data.get("case", {}),
        data.get("cooling", {})
    ]

    total_price = calculate_price(components)

    Build.objects.create(
        user=request.user,
        sector=sector,
        cpu=data.get("cpu", {}).get("name", ""),
        gpu=data.get("gpu", {}).get("name", ""),
        ram=data.get("ram", {}).get("name", ""),
        motherboard=data.get("motherboard", {}).get("name", ""),
        storage=data.get("storage", {}).get("name", ""),
        psu=data.get("psu", {}).get("name", ""),
        case=data.get("case", {}).get("name", ""),
        cooling=data.get("cooling", {}).get("name", ""),
        total_price=total_price
    )

    return JsonResponse({"status": "saved"})


@login_required
def edit_build(request, build_id):

    build = get_object_or_404(Build, id=build_id, user=request.user)

    return redirect(f"/builder/?sector={build.sector}&edit={build.id}")


@login_required
def my_builds(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    builds = Build.objects.filter(user=request.user)

    return render(request, "my_builds.html", {"builds": builds})


@login_required
def checkout(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":

        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")

        cpu = request.POST.get("cpu")
        gpu = request.POST.get("gpu")
        ram = request.POST.get("ram")
        storage = request.POST.get("storage")
        motherboard = request.POST.get("motherboard")
        psu = request.POST.get("psu")
        case = request.POST.get("case")
        cooling = request.POST.get("cooling")

        total_price = request.POST.get("total_price", 0)

        Order.objects.create(
            user=request.user,
            cpu=cpu,
            gpu=gpu,
            ram=ram,
            motherboard=motherboard,
            storage=storage,
            psu=psu,
            case=case,
            cooling=cooling,
            total_price=total_price,
            name=name,
            address=address,
            city=city,
            phone=phone,
            payment_method=payment_method
        )

        messages.success(request, "Order placed successfully")

        return render(request, "checkout.html", {"order_success": True})

    return render(request, "checkout.html")


@login_required
def my_orders(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "my_orders.html", {"orders": orders})


@login_required
def delete_build(request, build_id):

    build = get_object_or_404(Build, id=build_id, user=request.user)
    build.delete()

    return redirect("my_builds")


@staff_member_required
def admin_dashboard(request):

    total_orders = Order.objects.count()

    total_revenue = Order.objects.aggregate(
        Sum("total_price")
    )["total_price__sum"] or 0

    total_profit = Order.objects.aggregate(
        Sum("profit")
    )["profit__sum"] or 0

    total_users = User.objects.count()

    pending_orders = Order.objects.filter(status="Pending").count()
    processing_orders = Order.objects.filter(status="Processing").count()
    shipped_orders = Order.objects.filter(status="Shipped").count()
    delivered_orders = Order.objects.filter(status="Delivered").count()

    recent_orders = Order.objects.order_by("-created_at")[:5]

    return render(request, "admin_dashboard.html", {
        "orders": total_orders,
        "revenue": total_revenue,
        "profit": total_profit,
        "users": total_users,
        "pending": pending_orders,
        "processing": processing_orders,
        "shipped": shipped_orders,
        "delivered": delivered_orders,
        "recent_orders": recent_orders
    })


def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        Profile.objects.create(
            user=user,
            phone=phone
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("home")

    return render(request, "registration/signup.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("home")

        messages.error(request, "Invalid username or password")
        return redirect("home")

    return redirect("home")


def user_logout(request):

    logout(request)
    messages.success(request, "Logged out successfully")

    return redirect("home")