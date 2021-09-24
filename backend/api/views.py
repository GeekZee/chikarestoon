from rest_framework.viewsets import ModelViewSet

from .models import Ideas, Stars, UserInfo
from .serializer import IdeasSerializers

# Create your views here.

class IdeasViewSet(ModelViewSet):
    
    serializer_class = IdeasSerializers
    queryset = Ideas.objects.all()

    filterset_fields = ['category_ides', 'idea_writer']
    search_fields = [
        'title',
        'text',
        'category_ides',
        'idea_writer',
        'author__last_name',
    ]
    ordering_fields = ['id', 'date', 'category_ides', 'idea_writer']
    ordering = ['-date']  # ! default = new to old





