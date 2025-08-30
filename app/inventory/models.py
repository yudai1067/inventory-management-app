from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()


class Inventory(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
