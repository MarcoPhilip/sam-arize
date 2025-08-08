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


# Asset Model
class Asset(models.Model):
    STATUS_CHOICES = [
        ()
    ]

# Inventory Model


# Category Model


# Location Model


# Purchase Order Model


# Supplier Model