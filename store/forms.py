from datetime import timezone

from django import forms
from django.db.models import Max

from store.models import Auction, Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['start_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'type': 'datetime-local'})
        }


class BidForm(forms.ModelForm):
    amount = forms.DecimalField(min_value=0, max_digits=12, decimal_places=2)

    class Meta:
        model = Bid
        fields = ('amount',)

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        if amount and amount <= self.auction.artwork.price:
            raise forms.ValidationError("Bid amount must be greater than or equal to the starting bid.")
        highest_bid = Bid.objects.filter(auction=self.auction).aggregate(Max('amount'))['amount__max']
        if highest_bid and amount and amount <= highest_bid:
            raise forms.ValidationError("Bid amount must be greater than the current highest bid.")
        return cleaned_data

    def save(self, commit=True):
        bid = super().save(commit=False)
        bid.user = self.user
        bid.auction = self.auction
        if commit:
            bid.save()
        return bid