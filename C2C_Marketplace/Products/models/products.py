from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from django.conf import settings

class ListingType(models.TextChoices):
    SALE = "sale", "Sale"
    RENT = "rent", "Rent"

class PaymentOption(models.TextChoices):
    CASH = "cash", "Cash"
    EXCHANGE = "exchange", "Exchange"
    INSTALLMENTS = "installments", "Installments"
    CASH_OR_INSTALLMENTS = (
        "cash_or_installments",
        "Cash Or Installments"
    )


class Product(
    TitleDescriptionModel
):

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT
    )

    contactInfo = models.ForeignKey(
        "ContactInfo",
        on_delete=models.PROTECT
    )

    location = models.ForeignKey(
        "Location",
        on_delete=models.PROTECT
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    payment_option = models.CharField(
        max_length=50,
        choices=PaymentOption.choices
    )

    listing_type = models.CharField(
        max_length=50,
        choices=ListingType.choices
    )

    price = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    is_negotiable = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title
    
    
class ProductAttributeValue(models.Model):

    product = models.ForeignKey(
        "Product",
        related_name="attribute_values",
        on_delete=models.CASCADE
    )

    attribute = models.ForeignKey(
        "CategoryAttribute",
        on_delete=models.CASCADE
    )

    value = models.TextField()