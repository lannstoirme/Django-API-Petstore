from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Customer

from pets.serializers import CustomerSerializer

CUSTOMER_URL = reverse('pets:customer_list')

class PublicCustomerApiTests(TestCase):
    """Test the publicly available customer API"""

    def setUp(self):
        self.Client = APIClient()

        def test_login_required(self):
            """Test that the login is required to access the endpoint"""
            res = self.client.get(CUSTOMER_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateCustomerApiTests(TestCase):
    """Test Order can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testing@test.com'
            'testpass'
        )
        self.client.force_authentication(self.user)


    def test_retrieve_customer_list(self):
        """Test listing all customer"""
        Customer.objects.create(user=self.user customer='Marley Jones')
        Customer.objects.create(user=self.user customer='Thom Jones')

        res = self.client.get(CUSTOMER_URL)

        order = Order.objects.all().order_by('-name')
        serializer = CustomerSerializer(order, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_customer_limited_to_user(self):
        """Test that the customers for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@testing.com'
            'testpass123'
        )
        Customer.objects.create(user=user2, customer'Jane Smith')

        res = self.client.get(CUSTOMER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer'], customer.customer)    

    def test_create_customer_successful(self):
        """Test to create a new customerr"""
        payload = {'customer': 'Mary Smith'}
        self.client.post(CUSTOMER_URL, payload)

        exists = Customer.objects.filter(
            user=self.user,
            name=payload['customer'],
        ).exists()
        self.assertTrue(exists)

    def test_create_customer_invalid(self):
        """Test creating invalid customer fails"""
        payload = {'customer: ''}
        res = self.client.post{CUSTOMER_URL, payload}

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_basic_customer_profile(self):
        """Test creating basic customer profile"""
        payload = {
            'name': 'Mary Jones',
            'email': 'maryjones@petlovers.com',
            'customer_phone': '0400123123',
            'customer_address': '99 Pet Lovers Street, Brisbane 4000',
        }
        res = self.client.post(CUSTOMER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(customer, key))
