from django.contrib import admin
from .models import HairProduct


@admin.register(HairProduct)
class HairProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'category', 'price', 'curl_pattern', 'hair_type', 'vegan', 'weight',
                    'helpful_areas']
    search_fields = ['brand', 'name', 'category', 'curl_pattern', 'hair_type']
