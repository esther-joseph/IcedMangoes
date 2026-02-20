"""Store forms."""
from decimal import Decimal

from django import forms

from .models import Artist, Artwork


class ArtworkEditForm(forms.Form):
    """Form for updating an artwork."""

    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(max_length=500, required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0"), required=True)
    artist_name = forms.CharField(max_length=100, required=True)
    available = forms.BooleanField(required=False, initial=True)
    image = forms.ImageField(required=False)


class ArtworkForm(forms.Form):
    """Form for creating a new artwork."""

    image = forms.ImageField(
        required=True,
        help_text="Upload an image of your artwork",
    )
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(
        max_length=500,
        required=False,
        help_text="Comma-separated tags (e.g. abstract, oil, landscape)",
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0"),
        required=True,
        initial=Decimal("0.00"),
    )
    artist_name = forms.CharField(max_length=100, required=True)
