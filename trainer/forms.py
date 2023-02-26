from django import forms
from .models import Line, Opening, Variation

class OpeningForm(forms.ModelForm):
    class Meta:
        model = Opening
        fields = ['name', 'eco']

class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = ['name']

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['name', 'fen', 'pgn', 'line']