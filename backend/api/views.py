from rest_framework.viewsets import ModelViewSet

from .models import Ideas, Stars, UserInfo
from .serializer import IdeasSerializers

# Create your views here.

class IdeasViewSet(ModelViewSet):
    
    serializer_class = IdeasSerializers
    queryset = Ideas.objects.all()

    filterset_fields = ['category_ides', 'author', 'author__username']
    search_fields = ['title', 'text']
    ordering_fields = ['id', 'date', 'category_ides', 'author']
    ordering = ['-date']  # ! default = new to old





