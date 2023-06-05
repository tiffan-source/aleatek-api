from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import RapportVisiteSerializer, AvisOuvrageSerializer, CommentaireAvisOuvrageSerializer
from .models import RapportVisite, AvisOuvrage, CommentaireAvisOuvrage
from .permissions import IsAdminAuthenticated
# Create your views here.
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from rest_framework.response import Response

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class RapportVisiteSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = RapportVisiteSerializer
    queryset = RapportVisite.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AvisOuvrageViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisOuvrageSerializer
    queryset = AvisOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]

class CommentaireAvisOuvrageViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentaireAvisOuvrageSerializer
    queryset = CommentaireAvisOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class GetAllRapportVisiteByAffaire(APIView):
    def get(self, request, affaire):
        all_avis = RapportVisite.objects.filter(affaire=affaire)
        data = []
        for avis in all_avis:
            pre = model_to_dict(avis)
            pre['redacteur_detail'] = model_to_dict(avis.redacteur)
            data.append(pre)

        return Response(data)
    
class GetAllRapportVisiteOneVersions(APIView):
    def get(self, request, rv):
        avis = RapportVisite.objects.get(id=rv)
        pre = model_to_dict(avis)
        pre['redacteur_detail'] = model_to_dict(avis.redacteur)

        return Response(pre)