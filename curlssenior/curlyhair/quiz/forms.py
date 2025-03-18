# quiz/forms.py

# forms.py
from django import forms

from django import forms
from django import forms
from .models import TriedProduct


from django import forms
from .models import TriedProduct


class HairQuizForm(forms.Form):
    HAIR_TYPES = [
        ('Thin', 'Thin'),
        ('Medium', 'Medium'),
        ('Thick', 'Thick'),
    ]

    CURL_PATTERNS = [
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C'),
        ('3A', '3A'), ('3B', '3B'), ('3C', '3C'),
        ('4A', '4A'), ('4B', '4B'), ('4C', '4C'),
    ]

    MAINTENANCE_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    PRICE_RANGES = [
        ('$', '$ (Under $12)'),
        ('$$', '$$ ($12.01 - $25)'),
        ('$$$', '$$$ (Above $25)'),
    ]

    STYLING_PRODUCTS = [
        ('Mousse', 'Mousse'),
        ('Gel', 'Gel'),
    ]

    GROWTH_AREAS = [
        ('Hydrating', 'Hydrating'),
        ('Conditioning', 'Conditioning'),
        ('Moisturizing', 'Moisturizing'),
        ('Clarifying', 'Clarifying'),
        ('Damage Control', 'Damage Control'),
        ('Strengthening', 'Strengthening'),
        ('Repair', 'Repair'),
        ('Definition', 'Definition'),
    ]

    hair_type = forms.ChoiceField(choices=HAIR_TYPES, label="Hair Type")
    curl_pattern = forms.ChoiceField(choices=CURL_PATTERNS, label="Curl Pattern")
    vegan = forms.BooleanField(required=False, label="Vegan")
    maintenance_level = forms.ChoiceField(choices=MAINTENANCE_LEVELS, label="Maintenance Level")
    price_range = forms.ChoiceField(choices=PRICE_RANGES, label="Price Range")
    styling_product = forms.ChoiceField(choices=STYLING_PRODUCTS, label="Preferred Styling Product")
    growth_areas = forms.MultipleChoiceField(choices=GROWTH_AREAS, label="Hair Growth & Care Focus", required=False, widget=forms.CheckboxSelectMultiple())  # ✅ Add this line

    def clean_hair_type(self):
        data = self.cleaned_data['hair_type']
        return data

    def clean_curl_pattern(self):
        data = self.cleaned_data['curl_pattern']
        return data

    def clean_vegan(self):
        data = self.cleaned_data['vegan']
        return data

    def clean_weight(self):
        data = self.cleaned_data['weight']
        return data

from django import forms
from .models import TriedProduct

class TriedProductForm(forms.ModelForm):
    class Meta:
        model = TriedProduct
        fields = ['product', 'rating', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

