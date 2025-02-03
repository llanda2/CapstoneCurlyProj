# quiz/forms.py
from django import forms


class HairQuizForm(forms.Form):
    hair_type = forms.ChoiceField(
        choices=[('2A', '2A'), ('2B', '2B'), ('2C', '2C'), ('3A', '3A'),
                 ('3B', '3B'), ('3C', '3C'), ('4A', '4A'), ('4B', '4B'), ('4C', '4C')],
        widget=forms.RadioSelect,
        label="What is your hair type?"
    )
    curl_pattern = forms.ChoiceField(
        choices=[('Loose', 'Loose'), ('Tight', 'Tight'), ('Coiled', 'Coiled')],
        widget=forms.RadioSelect,
        label="What is your curl pattern?"
    )
    vegan = forms.BooleanField(
        required=False,
        label="Do you prefer vegan products?"
    )
    weight = forms.ChoiceField(
        choices=[('L', 'Light'), ('M', 'Medium'), ('H', 'Heavy')],
        widget=forms.RadioSelect,
        label="How much weight do you prefer in hair products?"
    )

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
