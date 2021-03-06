import csv
from pathlib import Path
from typing import List, Optional, Union

from django.core.management.base import BaseCommand, CommandError

from customer_geocoder.api.models import Customer
from customer_geocoder.api.utils.geolocation import lat_lng_by_address


def create_customer(
    header: List[str],
    customer: List[Union[str, float, int]],
    geocode: Optional[bool] = False
) -> Customer:
    """
    Creates a Customer object from a csv entry.

    Parameters
    ----------
    header : list of str
        csv header, with names of columns
    customer : list of values
        csv row with values
    geocode : bool, optional
        wether to geocode the customers

    Returns
    -------
    Customer
        customer with geolocated address
    """
    customer = dict(zip(header, customer))
    if geocode:
        address = f'{customer.get("company")}, {customer.get("city")}'
        lat_lon = lat_lng_by_address(address)
        lat_lon['latitude'] = lat_lon.pop('lat')
        lat_lon['longitude'] = lat_lon.pop('lng')
        customer = {**customer, **lat_lon}
    customer['latitude'] = customer.get('latitude') or None
    customer['longitude'] = customer.get('longitude') or None
    return Customer(**customer)


class Command(BaseCommand):
    """Django manager command to populate db from a csv file."""

    help = 'Adds customers from csv file'

    def add_arguments(self, parser):
        """Adds file_path to parser."""
        parser.add_argument('file_path', type=Path)
        parser.add_argument(
            '--geocode',
            action='store_true',
            help='Geocode customers from address',
        )

    def handle(self, *args, **options):
        """
        Handles command.

        Verifies if the path exists. Loads the csv file and create customers from each row.
        Adds all customers to the db.

        Raises
        ------
        ComandError
            exits if file_path doesnt exists
        """
        file_path = options['file_path']
        geocode = options['geocode']
        if not file_path.exists():
            raise CommandError(f'File {file_path} not found')
        with open(file_path) as f:
            data = csv.reader(f, delimiter=',', quotechar='"')
            header = next(data)
            self.stdout.write(self.style.WARNING('Loading and Geocoding customers'))
            customers = [create_customer(header, customer, geocode) for customer in data]
            self.stdout.write(self.style.WARNING('Saving customers do db'))
            Customer.objects.bulk_create(customers)
        self.stdout.write(self.style.SUCCESS(f'Successfully wrote csv {file_path} to db'))
