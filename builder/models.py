from django.db import models
from django.contrib.auth.models import User


class Component(models.Model):

    CATEGORY_CHOICES = [
        ('cpu', 'CPU'),
        ('gpu', 'GPU'),
        ('ram', 'RAM'),
        ('storage', 'Storage'),
        ('motherboard', 'Motherboard'),
        ('psu', 'PSU'),
        ('case', 'Case'),
        ('cooling', 'Cooling')
    ]

    SECTOR_CHOICES = [
        ('Gaming', 'Gaming'),
        ('Students', 'Students'),
        ('IT', 'IT'),
        ('Creators', 'Creators')
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    price = models.IntegerField()

    socket = models.CharField(max_length=50, blank=True)
    ram_type = models.CharField(max_length=50, blank=True)
    power = models.IntegerField(default=0)

    image = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Build(models.Model):

    SECTOR_CHOICES = [
        ('Gaming', 'Gaming'),
        ('Students', 'Students'),
        ('IT', 'IT'),
        ('Creators', 'Creators')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 🔥 NEW FIELD (IMPORTANT)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default="Gaming")

    cpu = models.CharField(max_length=200, blank=True)
    gpu = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=200, blank=True)

    motherboard = models.CharField(max_length=200, blank=True)
    storage = models.CharField(max_length=200, blank=True)

    psu = models.CharField(max_length=200, blank=True)
    case = models.CharField(max_length=200, blank=True)
    cooling = models.CharField(max_length=200, blank=True)

    total_price = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Build #{self.id} - {self.user.username}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cpu = models.CharField(max_length=200, blank=True)
    gpu = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=200, blank=True)

    motherboard = models.CharField(max_length=200, blank=True)
    storage = models.CharField(max_length=200, blank=True)

    psu = models.CharField(max_length=200, blank=True)
    case = models.CharField(max_length=200, blank=True)
    cooling = models.CharField(max_length=200, blank=True)

    total_price = models.IntegerField(default=0)

    name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    payment_method = models.CharField(max_length=50, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    profit = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    estimated_delivery = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username