from django.db import models

class ContactMethod(models.TextChoices):
    
    PHONE = "phone", "Phone"
    CHAT = "chat", "Chat"
    BOTH = "both", "Both"

class ContactInfo(models.Model):

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    contact_method = models.CharField(
        max_length=20,
        choices=ContactMethod.choices,
        default=ContactMethod.PHONE
    )

    def __str__(self):
        return self.name