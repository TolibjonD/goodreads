from django import forms
from .models import Books, BookReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('comment' , 'stars_given')