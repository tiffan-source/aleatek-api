from django.shortcuts import render
from .permissions import IsAdminAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import RICTSerializer, DispositionSerializer, AvisArticleSerializer, CommentaireAvisArticleSerializer, DescriptionSommaireSerializer, MissionRICTSerializer
from .models import RICT, Disposition, AvisArticle, CommentaireAvisArticle, DescriptionSommaire, MissionRICT
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.db import transaction
from rest_framework import status
from mission.models import ArticleMission, MissionActive
# Create your views here.

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()



class RICTViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = RICTSerializer
    queryset = RICT.objects.all()
    permission_classes = [IsAdminAuthenticated]

class DispositionViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DispositionSerializer
    queryset = Disposition.objects.all()
    permission_classes = [IsAdminAuthenticated]

class AvisArticleViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisArticleSerializer
    queryset = AvisArticle.objects.all()
    permission_classes = [IsAdminAuthenticated]

class CommentaireAvisArticleViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentaireAvisArticleSerializer
    queryset = CommentaireAvisArticle.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DescriptionSommaireViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DescriptionSommaireSerializer
    queryset = DescriptionSommaire.objects.all()
    permission_classes = [IsAdminAuthenticated]
    
class MissionRICTViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionRICTSerializer
    queryset = MissionRICT.objects.all()
    permission_classes = [IsAdminAuthenticated]


class CheckRICTForAffaire(APIView):
    def get(self, request, id_affaire):
        try:
            rict = RICT.objects.get(affaire=id_affaire)
            return Response(model_to_dict(rict))
        except:
            return Response(False)
        
class GetAllDispositionByRICTandMission(APIView):
    def get(self, request, id_rict, id_mission):
        dispositions = Disposition.objects.filter(rict=id_rict)
        data = []
        for disposition in dispositions:
            if disposition.article.mission.id == id_mission:
                data.append(model_to_dict(disposition))
        return Response(data)
        
class GetAllAvisByRICTandMission(APIView):
    def get(self, request, id_rict, id_mission):
        all_avis = AvisArticle.objects.filter(rict=id_rict)
        data = []
        for avis in all_avis:
            if avis.article.mission.id == id_mission:
                prepare = model_to_dict(avis)
                prepare['commentaires'] = []
                commentaires = CommentaireAvisArticle.objects.filter(id_avis=avis.id)
                for commentaire in commentaires:
                    prepare['commentaires'].append(model_to_dict(commentaire))
                data.append(prepare)
        return Response(data)
    
class GetDesriptionSommaireByRICT(APIView):
    def get(self, request, id_rict):
        descriptions = DescriptionSommaire.objects.filter(rict=id_rict)
        data = []

        for description in descriptions:
            data.append(model_to_dict(description))

        return Response(data)
    
class SaveDecriptionSommaire(APIView):
    def put(self, request):
        try:
            with transaction.atomic():
                descriptions = request.data['descriptions']
                
                for description in descriptions:
                    if 'id' in description:
                        description['rict_id'] = description.pop('rict')
                        DescriptionSommaire.objects.filter(id=description['id']).update(**description)
                    else:
                        DescriptionSommaire(**description).save()
            
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class SaveArticleDisposition(APIView):
    def post(self, request, rict, article, mission):
        try:
            with transaction.atomic():
                commentaire = request.data['commentaire']
                avis = request.data['avis']
                commentsAvis = request.data['commentAvis']
                
                id_avis = None
                
                article_mission = ArticleMission.objects.get(article=article, mission=mission)
                
                if Disposition.objects.filter(rict=rict, article=article_mission).exists():
                    Disposition.objects.filter(rict=rict, article=article_mission).update(commentaire=commentaire)
                else:
                    Disposition(rict_id=rict, article=article_mission, commentaire=commentaire).save()
                    
                if avis != 'false':
                    if AvisArticle.objects.filter(rict=rict, article=article_mission).exists():
                        AvisArticle.objects.filter(rict=rict, article=article_mission).update(codification=avis)
                    else:
                        AvisArticle(rict_id=rict, article=article_mission, codification=avis).save()
        
                    id_avis = AvisArticle.objects.get(rict=rict, article=article_mission).id
                else:
                    AvisArticle.objects.filter(rict=rict, article=article_mission).delete()
                    
                if id_avis:
                    CommentaireAvisArticle.objects.filter(id_avis=id_avis).delete()
                    for comment in commentsAvis:
                        CommentaireAvisArticle(id_avis_id=id_avis, commentaire=comment['commentaire'], a_suivre=comment['a_suivre']).save()
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class GetDisposionAvisAndComment(APIView):
    def get(self, request, rict, article, mission):
        try:
            data = {}
            
            article_mission = ArticleMission.objects.get(article=article, mission=mission)
            
            if Disposition.objects.filter(rict=rict, article=article_mission).exists():
                dispo = Disposition.objects.get(rict=rict, article=article_mission)
                data['disposition'] = model_to_dict(dispo)
                
            if AvisArticle.objects.filter(rict=rict, article=article_mission).exists():
                avis = AvisArticle.objects.get(rict=rict, article=article_mission)
                data['avis'] = model_to_dict(avis)
                data['avis']['commentaires'] = []
                for comment in CommentaireAvisArticle.objects.filter(id_avis=avis.id):
                    data['avis']['commentaires'].append(model_to_dict(comment))
                

        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(data, status=status.HTTP_200_OK)
    
class ValidateDevalidateMissionRict(APIView):
    def post(self, request, id_rict, id_mission):
        try:
            with transaction.atomic():
                validate = request.data['validate']
                rict = RICT.objects.get(id=id_rict)
                mission_active = MissionActive.objects.get(id_mission=id_mission, id_affaire=rict.affaire)
                if validate:
                    MissionRICT(rict=rict, mission=mission_active).save()
                else:
                    MissionRICT.objects.filter(rict=rict, mission=mission_active).delete()
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK)
    
class ValidateRICT(APIView):
    def put(self, request, id_rict):
        try:
            data = {}
            with transaction.atomic():
                exist = MissionRICT.objects.filter(rict=id_rict).exists()
                if exist:
                    RICT.objects.filter(id=id_rict).update(statut=1)
                    data['validate'] = True
                else:
                    data['validate'] = False
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_200_OK, data=data)
