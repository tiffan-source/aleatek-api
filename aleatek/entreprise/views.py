from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Responsable, Entreprise
from .permissions import IsAdminAuthenticated
from .serializers import ResponsableSerializer
from rest_framework.views import APIView


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ResponsableAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ResponsableSerializer
    queryset = Responsable.objects.all()
    permission_classes = [IsAdminAuthenticated]


from .serializers import EntrepriseSerializer


class EntrepriseAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseSerializer
    queryset = Entreprise.objects.all()
    permission_classes = [IsAdminAuthenticated]
