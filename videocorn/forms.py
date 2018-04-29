from django import forms
from .models import Genre, Year, Score, Actor, Movie
from django.forms import ModelForm

class SearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False)
    year = forms.ModelChoiceField(queryset=Year.objects.all(), required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)
    score = forms.ModelChoiceField(queryset=Score.objects.all(), required=False)
