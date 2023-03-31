from celery import shared_task
from django.utils import timezone
from .models import Auction

@shared_task
def check_auction_end_time():
    now = timezone.now()
    auctions = Auction.objects.filter(is_active=True, end_time__lt=now)
    for auction in auctions:
        auction.is_active = False
        auction.save()