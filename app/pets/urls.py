from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pets import views

router = DefaultRouter()
router.register('pets', views.PetViewSet)
router.register('order', views.OrderViewSet)
router.register('customer', views.CustomerViewSet)

app_name = 'pets'

urlpatterns = [
    path('', include(router.urls))
]