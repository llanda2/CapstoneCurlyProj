# quiz/forms.py

# forms.py
from django import forms

from django import forms
from django import forms
from .models import TriedProduct


from django import forms
from .models import TriedProduct

from django import forms

class HairQuizForm(forms.Form):
    MAINTENANCE_CHOICES = [
        ('high', 'High, I like to be pampered.'),
        ('medium', 'Medium, some pampering but not much.'),
        ('low', 'Low, keep it simple and easy.'),
    ]

    BUDGET_CHOICES = [
        ('$', '$12'),
        ('$$', '$12-25'),
        ('$$$', '$25+'),
    ]

    CURL_TYPE_CHOICES = [
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C'),
        ('3A', '3A'), ('3B', '3B'), ('3C', '3C'),
        ('4A', '4A'), ('4B', '4B'), ('4C', '4C'),
    ]

    VEGAN_CHOICES = [('yes', 'Yes'), ('no', 'No')]

    HAIR_LENGTH_CHOICES = [
        ('waist', 'To my waist'),
        ('mid_back', 'Mid back'),
        ('shoulders', 'Shoulders'),
        ('chin', 'Chin'),
    ]

    SCALP_CONDITION_CHOICES = [
        ('oily', 'Oily'),
        ('flaky', 'Flaky'),
        ('in_between', 'In between'),
        ('neither', 'Neither'),
    ]

    OILINESS_CHOICES = [
        ('1-2_days', '1-2 days'),
        ('3-4_days', '3-4 days'),
        ('week', 'A week'),
    ]

    HOLD_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]

    maintenance = forms.ChoiceField(choices=MAINTENANCE_CHOICES, widget=forms.RadioSelect)
    budget = forms.ChoiceField(choices=BUDGET_CHOICES, widget=forms.RadioSelect)
    curl_type = forms.ChoiceField(choices=CURL_TYPE_CHOICES, widget=forms.Select)
    vegan = forms.ChoiceField(choices=VEGAN_CHOICES, widget=forms.RadioSelect)
    hair_length = forms.ChoiceField(choices=HAIR_LENGTH_CHOICES, widget=forms.Select)
    scalp_condition = forms.ChoiceField(choices=SCALP_CONDITION_CHOICES, widget=forms.RadioSelect)
    oiliness = forms.ChoiceField(choices=OILINESS_CHOICES, widget=forms.RadioSelect)
    hold = forms.ChoiceField(choices=HOLD_CHOICES, widget=forms.RadioSelect)
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

