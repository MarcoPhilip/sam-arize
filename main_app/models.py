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

    def __str__(self):
        return self.name

# Location Model
class Location(models.Model):

    def __str__(self):
        return self.name
    

# Supplier Model
class Supplier(models.Model):

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
    category = models.ForeignKey(Category)
# Inventory Model







# Purchase Order Model


