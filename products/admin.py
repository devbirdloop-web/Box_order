from django.contrib import admin
from .models import Box


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'quality', 'is_active', 'created_at']
    list_filter = ['quality', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']