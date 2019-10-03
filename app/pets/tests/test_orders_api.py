from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Order

from pets.serializers import OrderSerializer

ORDER_URL = reverse('pets:order_list')

class PublicOrderApiTests(TestCase):
    """Test the publicly available order API"""

    def setUP(self):
        self.Client = APIClient()

        def test_login_required(self):
            """Test that login is required to access the endpoint"""
            res = self.client.get(ORDER_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateOrderApiTests(TestCase):
    """Test Order can be retrieved by authorised user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@testing.com'
            'testpass'
        )
        self.client.force_authentication(self.user)

    def test_retrieve_order_list(self):
        """Test listing all orders"""
        Order.objects.create(user=self.user, customer_name='Marley Jones')
        Order.objects.create(user=self.user, customer_name='Thom Jones')     

        res = self.client.get(ORDER_URL)

        order = Order.objects.all().order_by('-name')
        serializer = OrderSerializer(order, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_order_limited_to_user(self):
        """Test that the orders for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@testing.com'
            'testpass123'
        )
        Order.objects.create(user=user2, customer_name'Jane Smith')

        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer_name'], order.customer_name)    

    def test_create_order_successful(self):
        """Test to create a new order"""
        payload = {'customer_name': 'Mary Smith'}
        self.client.post(ORDER_URL, payload)

        exists = Order.objects.filter(
            user=self.user,
            name=payload['customer_name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_order_invalid(self):
        """Test creating invalid order fails"""
        payload = {'customer_name': ''}
        res = self.client.post{ORDER_URL, payload}

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_basic_order_profile(self):
        """Test creating basic order profile"""
        payload = {
            'customer_name': 'Jan Smith',
            'customer_phone': '0400123123',
            'customer_animal_choice': 'Kitten',
            'customer_budget': '200.00',
            'customer_allocated_preference': 'Harry the Kitten',
        }
        res = self.client.post(ORDER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Order.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(order, key))