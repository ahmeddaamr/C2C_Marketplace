from django.contrib import admin
from rest_framework.authtoken.models import Token
from .forms import (CustomUserCreationForm, CustomUserChangeForm)
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class CustomUserAdmin(DjangoUserAdmin):
    """Enhanced User admin with custom fields"""
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('id','username','email', 'first_name', 'last_name', 'phone', 'date_joined', 'is_superuser', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'nationality', 'SSN', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',  'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'deleted_at')}),
    )
    
    add_fieldsets = (
        (None, {'classes': ('wide',), 
                'fields': ('first_name', 'last_name','username', 'password1', 'password2',
                            'email', 'phone', 'nationality', 'SSN', 'birth_date'
                            ,'is_staff','is_superuser', #'groups',
                )}),
    )

    search_fields = ('email', 'username','SSN',)
    
    readonly_fields = ('is_superuser','last_login', 'date_joined', 'deleted_at','user_permissions')


admin.site.register(CustomUser, CustomUserAdmin)