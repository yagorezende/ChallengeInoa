import pandas as pd
from django.core.management import BaseCommand
from standard.models import Stock


class Command(BaseCommand):
    help = "Import B3 .csv file containing the companies symbol and name"

    def add_arguments(self, parser):
        parser.add_argument("--input", nargs=None, type=str)

    def handle(self, *args, **options):
        input_file = pd.read_csv(options["input"])
        for index, row in input_file.iterrows():
            stock, created = Stock.objects.get_or_create(
                company_name=row["Nome"],
                symbol=row["Ticker"],
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Stock {stock.symbol} - {stock.company_name} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Stock {stock.symbol} - {stock.company_name} already exists"))
