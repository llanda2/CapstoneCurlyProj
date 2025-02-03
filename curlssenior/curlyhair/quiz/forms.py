# quiz/forms.py
from django import forms

from django import forms


class HairQuizForm(forms.Form):
    HAIR_TYPE_CHOICES = [
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C'),
        ('3A', '3A'), ('3B', '3B'), ('3C', '3C'),
        ('4A', '4A'), ('4B', '4B'), ('4C', '4C'),
    ]

    MAINTENANCE_LEVEL_CHOICES = [
        ('low', 'Low (3-step routine)'),
        ('medium', 'Medium (4-step routine)'),
        ('high', 'High (5-step routine)'),
    ]

    hair_type = forms.ChoiceField(choices=HAIR_TYPE_CHOICES, label="What is your hair type?")
    vegan = forms.BooleanField(required=False, label="Do you prefer vegan products?")
    maintenance_level = forms.ChoiceField(choices=MAINTENANCE_LEVEL_CHOICES,
                                          label="How much maintenance do you prefer?")

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
