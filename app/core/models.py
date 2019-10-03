import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings



def pet_image_file_path(instance, filename):
    """Generate file path for new pet image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/pets/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



class PetManager(models.Model):
    """Manage Pet Inventory"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    def create_pet(self, name, in_store_status, category, price):
        pet = self.model(name, in_store_status, category, price)
        image = models.ImageField(null=True, upload_to=pet_image_file_path)
        pet.save(using=self._db)

        return self.pet


class StoreStatus(models.Model):
    """Status of Animal In Store Stock"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    STATUS_CHOICES = (
        ('Instore', 'Instore'),
        ('Onhold', 'Onhold'),
        ('SoldPendingPickup', 'SoldPendingPickup'),
        ('Returned', 'Returned'),
        ('PurchasedAndRehomed', 'PurchasedAndRehomed'),
        ('Ordered', 'Ordered'),
        )
    in_store_status = models.CharField(max_length = 30, choices = STATUS_CHOICES)
    

    def in_store(self):
        return self.in_store_status


class PetName(models.Model):
    """Allocated Name of the Animal"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    name = models.CharField(max_length=100),
        
    def __str__(self):
        return self.name

class Category(models.Model):
    """Category of Animal in the Store"""
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
            )
    CATEGORY_CHOICES = (
            ('Dog', 'Dog'),
            ('Cat', 'Cat'),
            ('Bird', 'Bird'),
            ('Rodent', 'Rodent'),
            ('Reptile', 'Reptile'),
            ('Fish', 'Fish'),
        )
    category = models.CharField(max_length = 100, choices = CATEGORY_CHOICES)

    def animal_category(self):
            return self.category

    
class Price(models.Model):
    """Price of Pet"""
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
            )
    def get_price(price):
            price = models.DecimalField(max_digits=8, decimal_places=2)

            return self.price

class Order(models.Model):
    """Customer Order Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    def create_order(self, user, customer_name, customer_phone, customer_animal_choice, customer_budget, customer_allocated_preference):
        order = self.model(user, customer_name, customer_phone, customer_animal_choice, customer_budget, customer_allocated_preference)
        customer_name = models.CharField(max_length=255)
        customer_phone = models.CharField(max_length=255)
        customer_animal_choice = models.CharField(max_length=255)
        customer_budget = models.DecimalField(max_digits=8, decimal_places=2)
        customer_allocated_preference = models.Charfield(max_length=255)

        return self.order

class Customer(models.Model):
    """Customer Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    def create_customer(self, user, name, email, customer_phone, customer_address):
        customer = self.model(self, user, name, email, customer_phone, customer_address)
        user = models.User
        name = models.CharField(max_length=255)
        email = models.CharField(max_length=255)
        customer_phone = models.CharField(max_length=255)
        customer_address = models.CharField(max_length=255)

        return self.customer

