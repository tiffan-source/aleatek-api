from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Collaborateurs
from .permissions import IsAdminAuthenticated
from .serializers import ColaboratteursSerializer
from rest_framework.views import APIView


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CollaborateursAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ColaboratteursSerializer
    queryset = Collaborateurs.objects.all()
    permission_classes = [IsAdminAuthenticated]


class UtilisateurConnecteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id
        }
        return Response(data)
