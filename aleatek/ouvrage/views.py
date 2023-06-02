from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Aso, AffaireOuvrage, Avis, Ouvrage, Documents, FichierAttache, RapportVisite
from .permissions import IsAdminAuthenticated
from .serializers import AsoSerializer, OuvrageSerializer, DocumentSerializer, FichierAttacheSerializer, \
    AvisSerializer, AffaireOuvrageSerializer, EntrepriseAffaireOuvrageSerializer
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from entreprise.models import Entreprise
from Dashbord.models import EntrepriseAffaire


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AsoSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AsoSerializer
    queryset = Aso.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AffaireOuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireOuvrageSerializer
    queryset = AffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class OuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = OuvrageSerializer
    queryset = Ouvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DocumentSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Documents.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AvisSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisSerializer
    queryset = Avis.objects.all()
    permission_classes = [IsAdminAuthenticated]


class FichierSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = FichierAttacheSerializer
    queryset = FichierAttache.objects.all()
    permission_classes = [IsAdminAuthenticated]
