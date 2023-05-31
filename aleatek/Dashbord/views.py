from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Produit, PlanAffaire, Affaire, Batiment, Chantier
from .permissions import IsAdminAuthenticated
from .serializers import AffaireSerializer, ProduitSerializer, PlanAffaireSerializer, BatimentSerializer, \
    ChantierSerializer
from rest_framework.views import APIView


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AffaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireSerializer
    queryset = Affaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class PlanAffaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = PlanAffaireSerializer
    queryset = PlanAffaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ProduitAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProduitSerializer
    queryset = Produit.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DestinationAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = BatimentSerializer
    queryset = Batiment.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ChantierAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ChantierSerializer
    queryset = Chantier.objects.all()
    permission_classes = [IsAdminAuthenticated]
