from django.db import models
# from Products_Service.utils.models.base import BaseModel


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
        "categories.Category",
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