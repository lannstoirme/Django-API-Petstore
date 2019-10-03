from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

def sample_pet(name='Fizzy', instore_status='PE', category='RP', price='120.79'):
    """Create a sample pet"""
    return get_pet_model().objects.create_pet(name, instore_status, category, price)

def sample_order(customer_name='Customer Test', customer_phone='0400123123',
                customer_animal_choice='Bird', customer_budget='100.00',
                customer_allocated_preference='Pet Name Izzy, Bird'):
    """Create a sample order"""
    return get_order_model().objects.create_order(customer_name, customer_phone,
                            customer_animal_choice, customer_budget,
                            customer_allocated_preference)

def sample_customer(customer='Loyalty Club Member', name='Mary Jones',
                        email='maryjones@petmail.com', customer_phone='0400123123',
                        customer_address='99 PetLovers Street, Brisbane 4000')
    """Create a sample customer"""
    return get_sample_customer().objects.create_customer(customer, name,
                                email, customer_phone, customer_address)



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@testing.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TESTING.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@testing.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_store_status_str(self):
        """Test the store status"""
       status = models.StoreStatus.create(
            user=sample_user(),
            pet=sample_pet(),
            in_store_status='Onhold'
        )

    def test_pet_name_str(self):
        """Test the pet name"""
        status = models.PetName.create(
            user=sample_user()
            pet=sample_pet()
            name='Buzz'
        )


    def test_pet_manager(self):
        """Test the Pet Manager Model"""
        pet = models.PetManager.objects.create(
            user=sample_user(),
            pet=sample_pet()
        )

        self.assertEqual(str(pet), pet.pet)

    def test_order_manager(self):
        """Test the Order Create Model"""
        order = models.Order.objects.create(
            user=sample_user(),
            pet=sample_pet()
            order=sample_order()
        )

        self.assertEqual(str(order), order.order)

    def test_customer(self):
        """Test the customer create model"""
        customer = models.Customer.objects.create(
            user=sample_user()
            customer=sample_customer()
        )

        self.asserEqual(str(customer), customer.customer)

    @patch('uuid.uuid4')
    def test_pet_file_name_uuid(self, mock_uuid):
        """Test that the image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.pet_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/pets/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
