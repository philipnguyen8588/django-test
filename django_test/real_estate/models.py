from django.db import models

from django.conf import settings


class SaleType(models.TextChoices):
    SALE = 'SALE', 'Sale'
    LEASE = 'LEASE', 'Lease'


class Status(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    SOLD = 'SOLD', 'Sold'
    LEASED = 'LEASED', 'Leased'
    DELETED = 'DELETED', 'Deleted'


class Property(models.Model):
    address = models.CharField(max_length=255)
    sale_type = models.CharField(
        max_length=10,
        choices=SaleType.choices,
        default=SaleType.SALE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
