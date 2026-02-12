"""
Shop models - same schema and intent as demo_205 Laravel (users, product_type, pay_type, products, transactions).
"""
from decimal import Decimal
from django.db import models
from django.conf import settings


class ProductType(models.Model):
    """Category / type of product (product_type table)."""
    type = models.CharField(max_length=32)

    class Meta:
        db_table = 'product_type'

    def __str__(self):
        return self.type


class PayType(models.Model):
    """Payment method (pay_type table)."""
    type = models.CharField(max_length=32)

    class Meta:
        db_table = 'pay_type'

    def __str__(self):
        return self.type


class Product(models.Model):
    """
    Product (book). Status: C=Create/Coming Soon, S=Sell/On Sale, D=Deleted.
    Same as Laravel products table.
    """
    STATUS_C = 'C'
    STATUS_S = 'S'
    STATUS_D = 'D'
    STATUS_CHOICES = [
        (STATUS_C, 'Coming Soon'),
        (STATUS_S, 'On Sale'),
        (STATUS_D, 'Deleted'),
    ]

    status = models.CharField(max_length=1, default=STATUS_C, choices=STATUS_CHOICES)
    name = models.CharField(max_length=80, blank=True, null=True, db_index=True)
    introduction = models.TextField(blank=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    remain_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name='products',
        db_column='product_type',
        default=1,
    )

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f'Product #{self.pk}'

    def get_photo_url(self, request=None):
        """URL for photo (proxy-safe if request available)."""
        if not self.photo:
            return ''
        from django.conf import settings
        prefix = getattr(settings, 'URL_PREFIX', '') or ''
        if prefix:
            return f"{prefix}{self.photo}"
        if self.photo.startswith('/'):
            return self.photo
        return f"/{self.photo.lstrip('/')}"


class Transaction(models.Model):
    """
    Order / purchase transaction. Same as Laravel transactions table.
    pay_type stored as FK to PayType (Laravel uses integer id in form, pay_type column).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transactions',
        db_column='user_id',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='transactions',
        db_column='product_id',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_count = models.IntegerField()
    total_price = models.DecimalField(max_digits=18, decimal_places=2)
    pay_type = models.ForeignKey(
        PayType,
        on_delete=models.PROTECT,
        related_name='transactions',
        db_column='pay_type',  # Laravel table uses column name pay_type storing id
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'Transaction #{self.pk}'
