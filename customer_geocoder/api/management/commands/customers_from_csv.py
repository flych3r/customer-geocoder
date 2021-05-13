import csv
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from customer_geocoder.api.models import Customer
from customer_geocoder.api.utils import geolocation


def create_customer(header, customer):
    customer = dict(zip(header, customer))
    lat_lon = geolocation.lat_lng_by_address(customer.get('city'))
    lat_lon['latitude'] = lat_lon.pop('lat')
    lat_lon['longitude'] = lat_lon.pop('lng')
    customer = {**customer, **lat_lon}
    return Customer(**customer)


class Command(BaseCommand):
    help = 'Adds heroes from csv file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=Path)

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not file_path.exists():
            raise CommandError(f'File {file_path} not found')
        with open(file_path) as f:
            data = csv.reader(f, delimiter=',', quotechar='"')
            header = next(data)
            self.stdout.write(self.style.WARNING('Loading and Geocoding customers'))
            customers = [create_customer(header, customer) for customer in data]
            self.stdout.write(self.style.WARNING('Saving customers do db'))
            Customer.objects.bulk_create(customers)
        self.stdout.write(self.style.SUCCESS(f'Successfully wrote csv {file_path} to db'))
