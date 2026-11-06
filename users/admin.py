from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'telefono', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'telefono')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (('Datos adicionales', {'fields': ('telefono',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Datos adicionales', {'fields': ('email', 'telefono')}),)
