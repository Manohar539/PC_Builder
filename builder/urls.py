# builder/urls.py

from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name="home"),

    # Builder
    path('builder/', views.pc_builder, name="builder"),

    # Build features
    path('save-build/', views.save_build, name="save_build"),

    # Checkout
    path('checkout/', views.checkout, name="checkout"),

    # User builds
    path('my-builds/', views.my_builds, name="my_builds"),
    path('delete-build/<int:build_id>/', views.delete_build, name="delete_build"),

    # Orders
    path('my-orders/', views.my_orders, name="my_orders"),
    path('edit-build/<int:build_id>/', views.edit_build, name="edit_build"),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),

    # Authentication
    path('accounts/signup/', views.signup, name="signup"),
    path('accounts/login/', views.user_login, name="login"),
    path('accounts/logout/', views.user_logout, name="logout"),
]