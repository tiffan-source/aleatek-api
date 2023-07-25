from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import SyntheseAvis
from .serializers import SyntheseAvisSerializer
from .permissions import IsAdminAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import date
from django.forms.models import model_to_dict
from commentaire.models import Commentaire
from rapport_visite.models import CommentaireAvisOuvrage
from RICT.models import CommentaireAvisArticle

# Create your views here.


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class SyntheseAvisViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = SyntheseAvisSerializer
    queryset = SyntheseAvis.objects.all()
    permission_classes = [IsAdminAuthenticated]

class CreateSyntheseAvis(APIView):
    def get(self, request, id_affaire):
        try:
            with transaction.atomic():
                all_avis = SyntheseAvis.objects.all()
                SyntheseAvis(affaire_id=id_affaire, createur=request.user, statut=0, order=len(all_avis)+1).save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
        
class AllSyntheseAvis(APIView):
    def get(self, request, id_affaire):
        all_synthese = SyntheseAvis.objects.filter(affaire=id_affaire)
        data = []
        for synthese in all_synthese:
            prepare = model_to_dict(synthese)
            prepare['createur'] = model_to_dict(synthese.createur)
            data.append(prepare)
        return Response(data)
