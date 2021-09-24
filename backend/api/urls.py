from django.urls.conf import include
from rest_framework import routers
from .views import UserViewSet, IdeasViewSet
from django.urls import path

app_name = 'api'


router = routers.SimpleRouter()
router.register('ideas', IdeasViewSet, basename="ideas")
router.register('users', UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
