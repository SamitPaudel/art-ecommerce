from django import forms
from store.models import Artwork


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artwork_title', 'medium_title', 'genre', 'height', 'width', 'description', 'price', 'image']
        labels = {
            'artwork_title': 'Artwork Title',
            'medium_title': 'Medium',
            'genre': 'Genre',
            'height': 'Height (in)',
            'width': 'Width (in)',
            'description': 'Description',
            'price': 'Price',
            'image': 'Artwork Image'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 1}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }