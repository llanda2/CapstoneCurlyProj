# quiz/forms.py

# forms.py
from django import forms


class HairQuizForm(forms.Form):
    HAIR_TYPE_CHOICES = [
        ('Thin', 'Thin'),
        ('Medium', 'Medium'),
        ('Thick', 'Thick'),
    ]

    CURL_PATTERN_CHOICES = [
        ('2A', '2A'),
        ('2B', '2B'),
        ('2C', '2C'),
        ('3A', '3A'),
        ('3B', '3B'),
        ('3C', '3C'),
        ('4A', '4A'),
        ('4B', '4B'),
        ('4C', '4C'),
    ]

    MAINTENANCE_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    hair_type = forms.ChoiceField(choices=HAIR_TYPE_CHOICES)
    curl_pattern = forms.ChoiceField(choices=CURL_PATTERN_CHOICES)
    vegan = forms.BooleanField(required=False)
    maintenance_level = forms.ChoiceField(choices=MAINTENANCE_LEVEL_CHOICES)
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
