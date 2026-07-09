from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from utils.models import BaseModel
# import uuid
    
class CustomUser(AbstractUser):

    phone = models.CharField(max_length=20,blank=False,help_text='+2010123456789')
    nationality = models.CharField(max_length=200,blank=False,default='Egyptian')
    SSN = models.CharField(max_length=14,unique=True,)
    birth_date = models.DateField(null=True, blank=True)
    # last_modified = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    # created_at = models.DateTimeField(auto_now_add=True) # same as date_joined

    # class Meta(AbstractUser.Meta):

    def soft_delete(self):
        self.deleted_at =  timezone.now()
        self.save(update_fields=['deleted_at'])

    @property
    def is_deleted(self):
        return self.deleted_at is not None
    
    def __str__(self):
        return self.get_full_name()

# class UserProfile(BaseModel):
#     """Extended user profile with metadata"""
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='profile'
#     )
#     phone = models.CharField(max_length=20,blank=False)
#     nationality = models.CharField(max_length=200,blank=False,default='Egyptian')
#     SSN = models.CharField(max_length=14,unique=True,)
#     birth_date = models.DateField(null=True, blank=True)

#     class Meta:
#         verbose_name = 'User Profile'
#         verbose_name_plural = 'User Profiles'
    
#     def __str__(self):
#         return f"{self.user.get_full_name() or self.user.username} - Profile" 
