from django import forms

from store.models import Auction, Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['start_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'type': 'datetime-local'})
        }

class BidForm(forms.ModelForm):
    auction_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Bid
        fields = ('auction_id', 'amount',)
        labels = {
            'amount': 'Bid Amount',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your bid amount'
            }),
        }

    def clean_auction_id(self):
        auction_id = self.cleaned_data['auction_id']
        try:
            auction = Auction.objects.get(id=auction_id)
        except Auction.DoesNotExist:
            raise forms.ValidationError("Invalid auction.")
        return auction

    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get('auction_id')
        amount = cleaned_data.get('amount')

        if auction and amount:
            highest_bid_amount = auction.get_highest_bid_amount() or auction.starting_price
            if amount <= highest_bid_amount:
                raise forms.ValidationError("Bid must be higher than the current highest bid")

        return cleaned_data

    def save(self, user):
        bid = super().save(commit=False)
        bid.user = user
        bid.auction_id = self.cleaned_data['auction_id']
        bid.amount = self.cleaned_data['amount']
        bid.save()
        return bid
