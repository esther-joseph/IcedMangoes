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
    """Form for creating a new artwork. Images handled via request.FILES.getlist('images')."""

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
    product_options = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="One per line: Product form, Price (e.g. Print 8x10, 25.00)",
    )
    artist_name = forms.CharField(max_length=100, required=True)
