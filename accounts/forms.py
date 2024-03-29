from django import forms
from .models import Account, ArtPortfolio

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'
    }
    ))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Re-enter Password'
    }
    ))

    class Meta:
        model = Account
        fields = ['full_name', 'email', 'phone_number', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError(
                'Passwords does not match'
            )

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("full_name", "username", "profileImage")

class ArtPortfolioForm(forms.ModelForm):
    class Meta:
        model = ArtPortfolio
        fields = ('image1', 'image2', 'image3', 'image4', 'image5')
        widgets = {
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

