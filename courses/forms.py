from django import forms
from .models import Chapter, Variation

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name', 'start_fen', 'course']

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['name', 'pgn', 'end_fen', 'chapter']