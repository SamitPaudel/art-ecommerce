# art_ecommerce/__init__.py

from art_ecommerce.celery import app as celery_app

__all__ = ('celery_app',)