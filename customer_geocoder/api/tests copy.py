from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from customer_geocoder.api.models import Customer


class CustomerTestCase(TestCase):
    """Test cases for Customer model."""

    def setUp(self):
        """Test cases setup."""
        User.objects.create_superuser('admin', 'test@email.com', 'admin')
        Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='e@mail.com',
            gender='Male',
            company='ACME',
            city='NY',
            title='Frontend Dev',
            latitude=-45,
            longitude=90
        )
        Customer.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='eletronic@mail.com',
            gender='Female',
            company='ACME',
            city='NY',
            title='Backend Dev',
            latitude=0.0,
            longitude=0.0
        )

    def test_super_user(self):
        """Super user can login."""
        client = Client()
        success = client.login(username='admin', password='admin')
        self.assertTrue(success)

    def test_all_customers(self):
        """All Customers are in db."""
        customers = Customer.objects.all()

        self.assertEqual(len(customers), 2)

    def test_get_customer(self):
        """Customers are correctly identified."""
        customer_1 = Customer.objects.get(first_name='John')
        customer_2 = Customer.objects.get(first_name='Jane')

        self.assertEqual(customer_1.email, 'e@mail.com')
        self.assertEqual(customer_2.email, 'eletronic@mail.com')
