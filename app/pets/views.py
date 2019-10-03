from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers

from core.models import User, PetManager, StoreStatus
from core.models import Category, Price, Order
from core.models import PetName
from core.models import Customer

from pets import serializers

class BasePetAttrViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Base viewset for user owned pet attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(pet__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

class PetViewSet(viewsets.ModelViewSet):
    """Manage pets in the database"""
    serializer_class = serializers.PetSerializer
    queryset = PetManager.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_inst(self, qs):
        """Convert a list of string IDS to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]
        if category:
            category_ids: self._params_to_ints(category)
            queryset = queryset.filter(category__id__in=category_ids)
        if in_store_status:
            in_store_status_ids = self_parama_to_ints(ingredients)
            queryset = queryset.filter(in_store_status__id__in=in_store_status_id)
    
    def get_queryset(self):
        """Retrieve the pets for the authenticated user"""
        category = self.request.query_params.get('category')
        in_store_status = self.request.query_params.get('in_store_status')
        queryset = self.queryset

        return self.queryset(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PetDetailSerializer
        elif self.action == 'upload_image':
            return serializers.PetImageSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Pet"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a pet"""
        pet = self.get_object()
        serializer = self.get_serializer(
            pet,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class OrderViewSet(viewsets.ModelViewSet):
    """Manage orders in the database"""
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the orders for the authenticated user"""
        return self.queryset(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.OrderDetailSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Order"""
        serializer.save(user=self.request.user)    

class CustomerViewSet(viewsets.ModelViewSet):
    """Manage customers in the database"""
    serializer_class = serializers.CustomerSerializer
    queryset = Customer.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the Customers for the authenticated user"""
        return self.queryset(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.CustomerDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Customer"""
        serializer.save(user=self.request.user)