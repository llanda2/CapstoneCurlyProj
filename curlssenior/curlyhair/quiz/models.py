# models.py
from django.db import models


class HairProduct(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    curl_pattern = models.CharField(max_length=255)
    hair_type = models.CharField(max_length=255)
    vegan = models.BooleanField()
    weight = models.CharField(max_length=1)  # L, M, H
    helpful_areas = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HairQuiz(models.Model):
    CURL_PATTERN_CHOICES = [
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C'), ('3A', '3A'),
        ('3B', '3B'), ('3C', '3C'), ('4A', '4A'), ('4B', '4B'), ('4C', '4C')
    ]
    HAIR_TYPE_CHOICES = [
        ('Thin', 'Thin'), ('Medium', 'Medium'), ('Thick', 'Thick')
    ]

    curl_pattern = models.CharField(max_length=3, choices=CURL_PATTERN_CHOICES)
    hair_type = models.CharField(max_length=6, choices=HAIR_TYPE_CHOICES)
    vegan_preference = models.BooleanField()

    def __str__(self):
        return f"{self.curl_pattern}, {self.hair_type}, {'Vegan' if self.vegan_preference else 'Non-Vegan'}"
