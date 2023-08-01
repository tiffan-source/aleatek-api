from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import SyntheseAvis, SyntheseCommentaireArticle, SyntheseComentaireRV, SyntheseCommentaireDocument
from .serializers import SyntheseAvisSerializer, SyntheseCommentaireDocumentSerializer, SyntheseComentaireRVSerializer, SyntheseCommentaireArticleSerializer
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
    
class SyntheseCommentaireDocumentViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = SyntheseCommentaireDocumentSerializer
    queryset = SyntheseCommentaireDocument.objects.all()
    permission_classes = [IsAdminAuthenticated]
    
class SyntheseComentaireRVViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = SyntheseComentaireRVSerializer
    queryset = SyntheseComentaireRV.objects.all()
    permission_classes = [IsAdminAuthenticated]
    
class SyntheseCommentaireArticleViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = SyntheseCommentaireArticleSerializer
    queryset = SyntheseCommentaireArticle.objects.all()
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


class GetAllCommentaireOnAffaire(APIView):
    def get(self, request, id_affaire):
        result = []
        
        # Commentaire sur document
        
        comment_docs = Commentaire.objects.filter(
            id_avis__id_document__emetteur__affaire_ouvrage__id_affaire__id=id_affaire,
            id_avis__id_document__aso__statut__gt=1)
        
        for comm in comment_docs:
            result.append({
                'lever' : comm.lever,
                'remarque' : comm.commentaire,
                'on' : "Aso numero " + str(comm.id_avis.id_document.aso.order_in_affaire),
                'ouvrage' : comm.id_avis.id_document.aso.affaireouvrage.id_ouvrage.libelle
            })
            
        # Commentaire sur RV
        
        comment_rv = CommentaireAvisOuvrage.objects.filter(
            avis__rv__affaire__id=id_affaire,
            avis__rv__statut__gt=1
        )
        
        for comm in comment_rv:
            result.append({
                'lever' : comm.lever,
                'remarque' : comm.commentaire,
                'on' : "RV numero " + str(comm.avis.rv.order_in_affaire),
                'ouvrage' : comm.avis.ouvrage.id_ouvrage.libelle
            })
            
        # Commentaire sur Article
        
        # comment_article = CommentaireAvisArticle.objects.filter(
        #     id_avis__rict__affaire__id=id_affaire,
        #     id_avis__rict__statut__gt=1
        # )
        
        # for comm in comment_article:
        #     result.append({
        #         'lever' : comm.lever,
        #         'remarque' : comm.commentaire,
        #         'on' : "RICT numero " + str(comm.rict.id),
        #         'ouvrage' : ""
        #     })

        return Response(result)