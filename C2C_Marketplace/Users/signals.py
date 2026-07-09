# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from .models import UserProfile


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Auto-create UserProfile and Token when a User is created"""
#     if created:
#         # UserProfile.objects.create(user=instance)
#         # Create auth token for REST API authentication
#         Token.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     """Save the user's profile whenever the user object is saved"""
#     if hasattr(instance, 'profile'):
#         instance.profile.save()
