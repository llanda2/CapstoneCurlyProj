from django import forms


class HairTypeForm(forms.Form):
    # List of hair types that the user can select
    HAIR_TYPES = [
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C'),
        ('3A', '3A'), ('3B', '3B'), ('3C', '3C'),
        ('4A', '4A'), ('4B', '4B'), ('4C', '4C')
    ]

    # MultipleChoiceField allows users to select multiple hair types
    curl_pattern = forms.MultipleChoiceField(
        choices=HAIR_TYPES,
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for selection
        required=True  # The user must select at least one curl pattern
    )

    # Add more fields here as needed (e.g., Weight, Vegan, etc.)
