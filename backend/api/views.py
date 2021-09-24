from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from .models import Ideas, Stars, UserInfo
from .serializer import IdeasSerializers, UserSerializers
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly, IsSuperUserOrStaffReadOnly

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

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsStaffOrReadOnly]
        else:
            permission_classes = [IsStaffOrReadOnly, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]




class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers
    permission_classes = (IsSuperUserOrStaffReadOnly,)
    filterset_fields = ['id', 'username', 'is_staff', 'is_active', 'email']
    ordering_fields = ['id', 'last_login', 'is_staff', 'date_joined']


