from celery import shared_task
from django.utils import timezone
from store.models import Auction

@shared_task
def check_ended_auctions():
    ended_auctions = Auction.objects.filter(
        is_active=True,
        end_time__lte=timezone.now()
    )
    for auction in ended_auctions:
        auction.end_auction()