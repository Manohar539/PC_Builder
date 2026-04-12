from django.contrib import admin
from .models import Component, Build, Order, Profile


# ----------------------------
# COMPONENT ADMIN
# ----------------------------

class ComponentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "sector",
        "price",
        "socket",
        "ram_type",
        "power"
    )

    list_filter = (
        "category",
        "sector"
    )

    search_fields = (
        "name",
    )

    ordering = ("category", "price")


# ----------------------------
# BUILD ADMIN
# ----------------------------

class BuildAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "cpu",
        "gpu",
        "ram",
        "total_price",
        "created_at"
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__username",
    )

    ordering = ("-created_at",)


# ----------------------------
# ORDER ADMIN
# ----------------------------

class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "total_price",
        "status",
        "payment_method",
        "profit",
        "created_at"
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "user__username",
        "cpu",
        "gpu"
    )

    ordering = ("-created_at",)

    list_editable = (
        "status",
        "profit",
    )


# ----------------------------
# PROFILE ADMIN
# ----------------------------

class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone"
    )

    search_fields = (
        "user__username",
    )


# REGISTER MODELS

admin.site.register(Component, ComponentAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)