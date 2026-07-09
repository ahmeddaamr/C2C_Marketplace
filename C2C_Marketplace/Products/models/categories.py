from django.utils import timezone
from django.db import models
# from utils.models.base import BaseModel
from django.utils.text import slugify


class Category(models.Model):

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

    path = models.CharField(
        max_length=255,
        db_index=True,
        blank=True
    )

    level = models.PositiveSmallIntegerField(
        default=1
    )

    icon = models.CharField(
        max_length=255,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )


    class Meta:
        ordering = ['path']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):

        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.name)

        # Calculate level before first save
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 1

        # First save to obtain ID
        super().save(*args, **kwargs)

        # Build path after ID exists
        new_path = (
            f"{self.parent.path}/{self.id}"
            if self.parent
            else str(self.id)
        )

        # Update path only if changed
        if self.path != new_path:
            self.path = new_path

            super().save(
                update_fields=['path']
            )

#EAV models for product attributes

class CategoryAttribute(models.Model):

    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    CHOICE = "choice"

    TYPE_CHOICES = [
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (BOOLEAN, "Boolean"),
        (CHOICE, "Choice"),
    ]

    category = models.ForeignKey(
        "Category",
        related_name="attributes",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    data_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    required = models.BooleanField(default=False)

    filterable = models.BooleanField(default=False)

    searchable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CategoryAttributeOption(models.Model):

    attribute = models.ForeignKey(
        "CategoryAttribute",
        related_name="options",
        on_delete=models.CASCADE
    )

    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value