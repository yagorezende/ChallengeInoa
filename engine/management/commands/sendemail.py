import pandas as pd
from dill import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from standard.models import Stock


class Command(BaseCommand):
    help = "Test send email configuration"

    def add_arguments(self, parser):
        parser.add_argument("--target", nargs=None, type=str)

    def handle(self, *args, **options):
        send_mail(
            subject='[Venda] INOA Stocks',
            message='Corpo do Email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[options.get('target')]
        )

