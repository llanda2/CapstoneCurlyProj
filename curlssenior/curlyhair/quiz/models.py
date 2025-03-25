# models.py
from django.db import models


class HairProduct(models.Model):
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    curl_pattern = models.CharField(max_length=255)
    hair_type = models.CharField(max_length=255)
    vegan = models.BooleanField(default=False)
    weight = models.CharField(max_length=1, choices=[('L', 'Light'), ('M', 'Medium'), ('H', 'Heavy')])
    growth_areas = models.CharField(max_length=255, blank=True, null=True)  # Allows empty values
    sulfate_free = models.BooleanField(default=False)
    hold_level = models.CharField(max_length=10, choices=[('light', 'Light'), ('medium', 'Medium'), ('strong', 'Strong')], blank=True, null=True)
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
    hair_length = models.CharField(max_length=10, choices=[('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')])
    hold_preference = models.CharField(max_length=20,
                                       choices=[('Soft', 'Soft'), ('Medium', 'Medium'), ('Strong', 'Strong')])
    curl_pattern = models.CharField(max_length=3, choices=CURL_PATTERN_CHOICES)
    hair_type = models.CharField(max_length=6, choices=HAIR_TYPE_CHOICES)
    vegan_preference = models.BooleanField()
    vegan = models.BooleanField(default=False)
    maintenance_level = models.CharField(max_length=50,
                                         choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    price_range = models.CharField(max_length=3, choices=[('$', 'Budget'), ('$$', 'Mid-Range'), ('$$$', 'High-End')])

    # New lifestyle factors
    hair_length = models.CharField(
        max_length=10,
        choices=[('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')],
        blank=True, null=True  # Allow existing rows to be NULL
    )

    hold_preference = models.CharField(
        max_length=20,
        choices=[('Soft', 'Soft'), ('Medium', 'Medium'), ('Strong', 'Strong')],
        blank=True, null=True  # Allow NULL values
    )

    scalp_condition = models.CharField(max_length=10,
                                       choices=[('Oily', 'Oily'), ('Flaky', 'Flaky'), ('Balanced', 'Balanced')])
    oiliness_timing = models.CharField(max_length=50,
                                       choices=[('1 day', '1 day'), ('2 days', '2 days'), ('3+ days', '3+ days')])
    wash_frequency = models.CharField(max_length=50, choices=[('Daily', 'Daily'), ('Every 2-3 days', 'Every 2-3 days'),
                                                              ('Weekly', 'Weekly')])
    hold_preference = models.CharField(max_length=20,
                                       choices=[('Soft', 'Soft'), ('Medium', 'Medium'), ('Strong', 'Strong')])

    # Updated styling product selection
    styling_product = models.CharField(max_length=10, choices=[('Mousse', 'Mousse'), ('Gel', 'Gel')])

    # Updated growth area selection
    growth_areas = models.CharField(
        max_length=20,
        choices=[
            ('Hydrating', 'Hydrating'),
            ('Conditioning', 'Conditioning'),
            ('Moisturizing', 'Moisturizing'),
            ('Clarifying', 'Clarifying'),
            ('Damage Control', 'Damage Control'),
            ('Strengthening', 'Strengthening'),
            ('Repair', 'Repair'),
            ('Definition', 'Definition')
        ],
        default='Hydrating'  # Add a default value
    )

    dyed_or_bleached = models.BooleanField(default=False)
    sensitive_scalp = models.BooleanField(default=False)
    prone_to_flakes = models.BooleanField(default=False)
    workout_frequency = models.CharField(max_length=20,
                                         choices=[('Rarely', 'Rarely'), ('1-2 times/week', '1-2 times/week'),
                                                  ('3+ times/week', '3+ times/week')])

    def __str__(self):
        return f"{self.hair_type} - {self.curl_pattern} Preferences"

    def __str__(self):
        return f"{self.curl_pattern}, {self.hair_type}, {'Vegan' if self.vegan_preference else 'Non-Vegan'}"


class TriedProduct(models.Model):
    product = models.ForeignKey(HairProduct, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[
        (1, "Awful, never again"),
        (2, "Not great"),
        (3, "Okay, would try again"),
        (4, "Good, recommend"),
        (5, "Amazing, holy grail product")
    ])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars"
