from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import commentaire
from .permissions import IsAdminAuthenticated
from .serializers import CommentaireSerializer
from rest_framework.views import APIView


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentaireSerializer
    queryset = commentaire.objects.all()
    permission_classes = [IsAdminAuthenticated]

