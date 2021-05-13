from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient

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

    def test_api_get_customers(self):
        """GET /customer/ returns all customers."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        self.assertContains(response, text='', status_code=200)
        resp_json = response.json()

        self.assertEqual(resp_json.get('count'), 2)
        self.assertEqual(len(resp_json.get('results')), 2)

        customer_1 = resp_json.get('results')[0]
        customer_2 = resp_json.get('results')[1]
        self.assertEqual(customer_1.get('first_name'), 'John')
        self.assertEqual(customer_2.get('first_name'), 'Jane')

        client.logout()

    def test_api_get_customer_id(self):
        """GET /customer/id/ returns single customer."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/1/')
        self.assertContains(response, text='', status_code=200)
        customer_1 = response.json()
        self.assertEqual(customer_1.get('first_name'), 'John')

        response = client.get('/customers/2/')
        self.assertContains(response, text='', status_code=200)
        customer_2 = response.json()
        self.assertEqual(customer_2.get('first_name'), 'Jane')

        client.logout()

    def test_api_post_customer_valid(self):
        """POST /customer/ creates new customer if data is valid."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        resp_json = response.json()
        before_post = resp_json.get('count')

        response = client.post(
            '/customers/',
            data={
                'first_name': 'Some',
                'last_name': 'Name',
                'email': 'some@email.com',
                'gender': 'Not informed',
                'company': 'ACME',
                'city': 'NY',
                'title': 'Fullstack Dev',
                'latitude': 90.0,
                'longitude': -180.0
            },
            format='json'
        )
        self.assertContains(response, text='', status_code=201)
        new_customer = response.json()

        response = client.get('/customers/')
        resp_json = response.json()
        after_post = resp_json.get('count')
        self.assertEqual(before_post + 1, after_post)

        response = client.get(f'/customers/{new_customer.get("id")}/')
        self.assertContains(response, text='', status_code=200)
        customer = response.json()
        self.assertEqual(customer.get('first_name'), 'Some')

        client.logout()

    def test_api_post_customer_invalid_email(self):
        """POST /customer/ creates fails if email is invalid."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        resp_json = response.json()
        before_post = resp_json.get('count')

        response = client.post(
            '/customers/',
            data={
                'first_name': 'Some',
                'last_name': 'Name',
                'email': 'email',
                'gender': 'Not informed',
                'company': 'ACME',
                'city': 'NY',
                'title': 'Fullstack Dev',
                'latitude': 90.0,
                'longitude': -180.0
            },
            format='json'
        )
        self.assertContains(response, text='', status_code=400)
        resp_json = response.json()

        self.assertEqual(resp_json, {'email': ['Enter a valid email address.']})

        response = client.get('/customers/')
        resp_json = response.json()
        after_post = resp_json.get('count')
        self.assertEqual(before_post, after_post)

        client.logout()

    def test_api_post_customer_invalid_lat_lng(self):
        """POST /customer/ creates fails if latitude, longitude is invalid."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        resp_json = response.json()
        before_post = resp_json.get('count')

        response = client.post(
            '/customers/',
            data={
                'first_name': 'Some',
                'last_name': 'Name',
                'email': 'some@email.com',
                'gender': 'Not informed',
                'company': 'ACME',
                'city': 'NY',
                'title': 'Fullstack Dev',
                'latitude': -180.0,
                'longitude': 360.0
            },
            format='json'
        )
        self.assertContains(response, text='', status_code=400)
        resp_json = response.json()
        self.assertEqual(
            resp_json,
            {
                'latitude': ['Ensure this value is greater than or equal to -90.0.'],
                'longitude': ['Ensure this value is less than or equal to 180.0.']
            }
        )

        response = client.get('/customers/')
        resp_json = response.json()
        after_post = resp_json.get('count')
        self.assertEqual(before_post, after_post)

        client.logout()

    def test_api_put_customer(self):
        """PUT /customer/id/ replaces customer data."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        resp_json = response.json()
        before_put = resp_json.get('count')

        response = client.put(
            '/customers/1/',
            data={
                'first_name': 'Hansel',
                'last_name': 'Gretel',
                'email': 'oficial@email.com',
                'gender': 'Not informed',
                'company': 'Globex',
                'city': 'NY',
                'title': 'CEO',
                'latitude': 0.0,
                'longitude': 0.0
            },
            format='json'
        )
        self.assertContains(response, text='', status_code=200)

        response = client.get('/customers/')
        resp_json = response.json()
        after_patch = resp_json.get('count')
        self.assertEqual(before_put, after_patch)

        response = client.get('/customers/1/')
        self.assertContains(response, text='', status_code=200)
        customer = response.json()
        self.assertEqual(customer.get('company'), 'Globex')

        client.logout()

    def test_api_patch_customer(self):
        """PATCH /customer/id updates customer data."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        resp_json = response.json()
        before_patch = resp_json.get('count')

        response = client.patch(
            '/customers/1/',
            data={
                'company': 'Globex',
            },
            format='json'
        )
        self.assertContains(response, text='', status_code=200)

        response = client.get('/customers/')
        resp_json = response.json()
        after_patch = resp_json.get('count')
        self.assertEqual(before_patch, after_patch)

        response = client.get('/customers/1/')
        self.assertContains(response, text='', status_code=200)
        customer = response.json()
        self.assertEqual(customer.get('company'), 'Globex')

        client.logout()

    def test_api_delete_customer(self):
        """DELETE /customer/ removes customer."""
        client = APIClient()
        client.login(username='admin', password='admin')
        response = client.get('/customers/')
        resp_json = response.json()
        before_delete = resp_json.get('count')

        response = client.delete('/customers/1/')
        self.assertContains(response, text='', status_code=204)

        response = client.get('/customers/')
        resp_json = response.json()
        after_delete = resp_json.get('count')
        self.assertEqual(before_delete - 1, after_delete)

        response = client.get('/customers/1/')
        self.assertContains(response, text='', status_code=404)

        client.logout()
