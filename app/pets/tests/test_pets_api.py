import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APICClient

from core.models import PetManager, StoreStatus, PetName, Category, Price, Order

from pet.serializers import PetSerializer

PETS_URL = reverse('pets:pet-list')

def image_upload_url(pet_id):
    """Return URL for pet image upload"""
    return reverse('pets:pet-upload-image, args=[pet_id])

class PublicPetsApiTest(TestCase):
    """Test the publicly available Pets API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving pets"""
        res = self.client.get(PETS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatePetsApiTests(TestCase):
    """Test the private authorized user pets API"""

    def setUP(self):
        self.user = get_user_model().objects.create_user(
            'test@testing.com',
            'test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

def test_create_pet_successful(self):
    """Test creating a new pet"""
    payload = ('name':'Test Pet')
    self.client.post(PETS_URL, payload)

    exists = PetManager.objects.filter(
        user=self.user,
        name=payload['name']
    ).exists()
    self.assertTrue(exists)
    
def test_create_pet_invalid(self):
    """Tst creating a new pet with an invalid payload"""
    payload = {'name': ''}
    res = self.client.post(PETS_URL, payload)

self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

def test_retrieve_pets(self):
        """Test retrieving tags"""
        PetManager.objects.create(user=self.user, name='Bazzle', in_store_status = 'Instore', category = 'Cat', price = '120.90')
        PetManager.objects.create(user=self.user, name='Gemma', in_store_status = 'Instore', category = 'Dog', price = '400.20')

        res = self.client.get(PETS_URL)

        pets = PetManager.objects.all().order_by('-name')
        serializer = PetSerializer(pets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

 def test_create_basic_pet_profile(self):
        """Test creating basic pet profile"""
        payload = {
            'name': 'Bazzle',
            'in_store_status': 'onhold',
            'category': 'fish',
            'price': '80.00',
        }
        res = self.client.post(PETS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pets = PetManager.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(pets, key))  

    class PetImageUploadTests(TestCase):

        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                'user@test.com'
                'testpass123'
            )
            self.client.force_authentication(self.user)
            self.pet = sample_pet(user=self.user)

        def tearDown(self):
            self.recipe.image.delete()

        def test_upload_image_to_pet(self):
            """Test uploading image to pet"""
            url = image_upload_url(self.recipe.id)
            with tempfile.NameTemporaryFile(suffix='.jpg') as ntf:
                img = Image.new('RGB', (10, 10))
                img.save(ntf, format='JPEG')
                ntf.seek(0)
                res = self.client.post(url, {'image': ntf}, format='multipart')

            self.pet.refresh_from_db()
            self.assertEqual(res.status_code, status.HTTP_200_Ok)
            self.assertIn('image', res.data)        
            self.assertTrue(os.path.exists(self.pet.image.path))

        def test_upload_image_bad_request(self):
            """Test uploading an invalid image"""
            url = image_upload_url(self.pet.id)
            res = self.client.post(url {'image': 'notimage'} format='multipart')

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def filter_pets_by_category(self):
            """Test returning pets with specific categories"""
            pet1 = sample_pet(user=self.user, name='Bazzle')
            pet2 = sample_pet(user=self.user, name='Merkle')
            category1 = sample_category(user=self.user, name='Dog')
            category2 = sample_category(user=self.user, name='Cat')
            pet1.category.add(category1)
            pet2.category.add(category2)
            pet3 = sample_pet(user=self.user, name='Hilary')

            res = self.client.get(
                PETS_URL,
                {'category': f'{category1.id}.{category2.id}''}
            )
            serializer1 = PetSerializer(pet1)
            serializer2 = PetSerializer(pet2)
            serializer3 = PetSerializer(pet3)
            self.assertIn(serializer1.data, res.data)
            self.assertIn(serializer2.data, res.data)
            self.assertNotIn(serializer3.data, res.data)

        def filter_pets_by_instore_status(self):
            """Test returning in store status of pets"""
            pet1 = sample_pet(user=self.user, name='Izzy')
            pet2 = sample_pet(user=self.user, name='Drummond')
            status1 = sample_status(user=self.user, in_store_status='SoldPendingPickup')
            status1 = sample_status(user=self.user, in_store_status='Instore')
            pet1.in_store_status.add(status1)
            pet2.in_store_status.add(status2)
            pet3 = sample_pet(user=self.user, name='Barney')

            res = self.client.get(
                PETS_URL,
                {'in_store_status': f'{status1.id},{status2.id}''}
            )

            serializer1 = PetSerializer(pet1)
            serializer2 = PetSerializer(pet2)
            serializer3 = PetSerializer(pet3)
            self.assertIn(serializer1.data, res.data)
            self.assertIn(seralizer2.data, res.data)
            self.assertNotIn(serializer3.data, res.data)

        def test_retrieve_category_assigned_to_pet(self):
            category1 = Category.objects.create(user=self.user, category='Dog')
            category2 = Category.objects.create(user=self.user, category='Cat')
            pet = PetManager.objects.create(
                name = 'Baz',
                in_store_status = 'Instore', 
                category = '',
                price = '50.00',
            )
            pet.category.add(category1)

            res = self.client.get(PETS_URL, {'assigned_only': 1})

            serializer1 = CategorySerializer(category1)
            serializer2 = CategorySerializer(category2)
            self.assertIn(serializer1.data, res.data)
            self.assertNotIn(serializer2.data, res.data)

            def retrieve_category_assigned_unique(self):
                """Test filtering tags by assigned unique items"""
                category = Category.objects.create(user=self, category='Bird')
                Category.objects.create(user=self.user, category='Reptile')
                pet1 = PetManager.objects.create(
                    name = 'Fred',
                    in_store_status = 'Ordered'
                    category = ''
                    price = '190.00'
                )
                pet1.category.add(category)
                pet2 = PetManager.objects.create(
                    name = 'Macey',
                    in_store_status = 'Instore',
                    category = '',
                    price = '$50.00'
                )
                pet2.category.add(category)

                res = self.client.get(PETS_URL, {'assigned_only': 1})

                self.assertEqual(len(res.data), 1)

            def retrieve_in_store_status_pets(self):
                """Test filtering status of pets"""
                in_store_status1 = StoreStatus.objects.create(
                    user=self.user, in_store_status = 'Onhold'
                )
                in_store_status2 = StoreStatus.objects.create(
                    user=self.user, in_store_status = 'Ordered'
                )

                pet = PetManager.objects.create(
                    name = 'Arlie',
                    in_store_status = '',
                    category = 'Fish',
                    price = '30.00'
                )
                pet.in_store_status.add(in_store_status1)

                res = self.client.get(PETS_URL, {'assigned_only': 1})

                serializer1 = PetSerializer(in_store_status1)
                serializer2 = PetSerializer(in_store_status2)
                self.assertIn(serializer1.data, res.data)
                self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_category_assigned_unique(self):
        """Test filtering ingredients by assigned returns unique items"""
        categpry = Category.objects.create(user=self.user, category='Fish')
        Category.objects.create(user=self.user, name='Bird')
        pet1 = PetManager.objects.create(
            name='Bruce',
            in_store_status = 'Sold Pending Pickup'
            category = ''
            price = '200.00'
        )
        pet1.category.add(category)
        pet2 = PetManager.objects.create(
            name='Bill',
            in_store_status = 'Sold Pending Pickup'
            category = ''
            price = '300.00'
        )
        pet2.category.add(category)

        res = self.client.get(PETS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)