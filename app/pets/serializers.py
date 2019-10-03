from rest_framework import serializers

from core.models import PetManager
from core.models import Customer
from core.models import StoreStatus
from core.models import PetName
from core.models import Category
from core.models import Price
from core.models import Order
from core.models import User
from core.models import UserManager



class PetSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = PetManager
        fields = ('id', 'name', 'in_store_status', 'category', 'price')
        read_only_fields = ('id',)

class PetDetailSerializer(PetSerializer):
    """Serialize a Pet Detail"""
    pet = PetSerializer(many=True, read_only=True)

class StoreStatusSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = StoreStatus
        fields = ('category')
        read_only_fields = ('id',)

class PetNameSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = PetName
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Category
        fields = ('id', 'category')
        read_only_fields = ('id',)

class PriceSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Price
        fields = ('id', 'price')
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Order
        fields = ('id', 'order', 'customer_name'
                'customer_phone', 'customer_animal_choice',
                'customer_budget', 'customer_allocated_preference')
        read_only_fields = ('id', 'order')

class OrderDetailSerializer(OrderSerializer):
    """Serialize an Order Detail"""
    order = OrderSerializer(many=True, read_only=True)

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customer objects"""

    class Meta:
        model = Customer
        fields = ('id', 'customer', 'user', 
                'name', 'email', 'customer_phone',
                 'customer_address')
        read_only_fields = ('id', 'customer', 'user')

class CustomerDetailSerializer(OrderSerializer):
    """Serialize a Customer in Detail"""
    customer = CustomerSerializer(many=True, read_only=True)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects"""

    class Meta:
        model = User
        fields = ('id', 'name', 'email')
        read_only_fields = ('id')

class PetImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to pets"""

    class Meta:
        model = PetManager
        fields = ('id', 'image')
        read_only_fields = ('id',)      