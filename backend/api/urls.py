from django.urls.conf import include
from rest_framework import routers
from .views import  IdeasViewSet
from django.urls import path

app_name = 'api'


router = routers.SimpleRouter()
router.register('ideas', IdeasViewSet, basename="ideas")

urlpatterns = [
    path("", include(router.urls)),
]
