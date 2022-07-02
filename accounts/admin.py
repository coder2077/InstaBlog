from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_pic',)}), 
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_pic',)}), 
    )

admin.site.register(CustomUser, CustomUserAdmin)
