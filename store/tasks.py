import threading

import pytz
from celery import shared_task
from django.utils import timezone

from store.models import Auction

@shared_task
def check_end_times():
    kathmandu_tz = pytz.timezone('Asia/Kathmandu')
    auctions = Auction.objects.filter(is_active=True)
    for auction in auctions:
        if auction.end_time >= timezone.localtime(timezone.now(), kathmandu_tz):
            auction.is_active = False
            auction.save()
