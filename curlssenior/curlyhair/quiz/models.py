from django.db import models


class HairProduct(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    curl_pattern = models.CharField(max_length=255)  # Stores multiple curl patterns
    hair_type = models.CharField(max_length=255)  # Stores multiple hair types
    vegan = models.BooleanField()
    weight = models.CharField(max_length=1)  # L, M, H
    helpful_areas = models.CharField(max_length=255)

    def __str__(self):
        return self.name
