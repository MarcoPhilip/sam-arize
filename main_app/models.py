from django.db import models

# ! Create your models here.

# User Model
class User(models.Model):
    # Define the roles
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff')
    ]

    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Location Model
class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField() 

    def __str__(self):
        return self.name
    

# Asset Model
class Asset(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('discontinued', 'Discontinued')
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    serial_number = models.CharField(100, unique=True)
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    

# Inventory Model
class Inventory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name






# Purchase Order Model


