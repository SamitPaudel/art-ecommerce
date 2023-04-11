from django import forms

from accounts.models import Account
from artist.models import Artist
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


class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('full_name', 'username', 'email', 'phone_number', 'password', 'confirm_password', 'profileImage')

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )

        return cleaned_data


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('artist_name', 'description')