from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_admin', 'created_at')
    search_fields = ('email', 'name')
    ordering = ('email',)
    list_filter = ('is_admin', 'is_active')

