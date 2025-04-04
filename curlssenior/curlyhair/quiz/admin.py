from django.contrib import admin
from .models import HairProduct

@admin.register(HairProduct)
class HairProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'category', 'price', 'curl_pattern', 'hair_type', 'vegan', 'weight', 'growth_areas')
