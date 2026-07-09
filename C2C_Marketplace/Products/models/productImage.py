from django.db import models

class ProductImage(models.Model):

    product = models.ForeignKey(
        "Product",
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="products/"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_primary = models.BooleanField(
        default=False
    )