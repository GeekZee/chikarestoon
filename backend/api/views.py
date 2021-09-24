from rest_framework.viewsets import ModelViewSet

from .models import Ideas, Stars, UserInfo
from .serializer import IdeasSerializers

# Create your views here.


class IdeasViewSet(ModelViewSet):

    serializer_class = IdeasSerializers
    queryset = Ideas.objects.all()

    filterset_fields = ['category', 'author', 'author__username']
    search_fields = ['title', 'text', 'slug',
                     'author__username',
                     'author__first_name',
                     'author__last_name',
                     ]
    ordering_fields = ['id', 'created', 'updated', 'category', 'author']
    ordering = ['-created']  # ! default = new to old
