from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer
from rest_framework.views import APIView


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class MissionAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()
    permission_classes = [IsAdminAuthenticated]


class MissionActiveAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionActiveSerializer
    queryset = MissionActive.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ITAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = InterventionTechniqueSerializer
    queryset = InterventionTechnique.objects.all()
    permission_classes = [IsAdminAuthenticated]
