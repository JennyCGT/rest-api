from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department,Roles

class CustomUserAdmin(UserAdmin):
    model = User
    list_display_links = ['email']
    search_fields = ('email',)
    ordering = ('email',)
    list_display = ('pk','email', 'is_staff', 'is_active','is_superuser')



admin.site.register(User, CustomUserAdmin)
