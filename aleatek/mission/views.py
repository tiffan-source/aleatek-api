from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique, Article, ArticleSelect
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer, ArticleSerializer, ArticleSelectSerializer
from rest_framework.views import APIView
from Dashbord.models import Affaire, PlanAffaire
from collaborateurs.models import Collaborateurs
from django.forms.models import model_to_dict
from rest_framework import status
from django.db import transaction


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

class ArticleAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAdminAuthenticated]

class ArticleSelectViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleSelectSerializer
    queryset = ArticleSelect.objects.all()
    permission_classes = [IsAdminAuthenticated]

class MissionActiveAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionActiveSerializer
    queryset = MissionActive.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ITAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = InterventionTechniqueSerializer
    queryset = InterventionTechnique.objects.all()
    permission_classes = [IsAdminAuthenticated]

class MissionActiveForCurrentAffaire(APIView):
    def get(self, request, id_affaire):
        all_mission_active = MissionActive.objects.filter(id_affaire=id_affaire).values()

        return Response(list(all_mission_active))
    
class VerifyExistITForMissionSignAndCollab(APIView):
    def get(self, request, id_collab, id_mission_sign):
        try:
            InterventionTechnique.objects.get(id_mission_active=id_mission_sign, id_collaborateur=id_collab)
            return Response({'check' : True})
        except:        
            return Response({'check' : False})
        
class VerifyExistMissionActive(APIView):
    def get(self, request, id_affaire, id_mission):
        try:
            mission = MissionActive.objects.get(id_mission=id_mission, id_affaire=id_affaire)
            return Response({'check' : mission.id})
        except:        
            return Response({'check' : False})
        
class AllIntervenantForAffaire(APIView):
    def get(self, request, id_affaire):
        all_collab = Collaborateurs.objects.all()
        all_IT = InterventionTechnique.objects.all()
        
        data = []
        
        for collab in all_collab:
            for IT in all_IT:
                if collab.id == IT.id_collaborateur.id:
                    missionActive = IT.id_mission_active
                    affaire = missionActive.id_affaire
                    if affaire.id == id_affaire:
                        data.append({
                            "id" : collab.id,
                            "nom" : collab.first_name,
                            "prenom" : collab.last_name,
                            "email" : collab.email
                        })

        return Response(data);

class AllMissionForAffaire(APIView):
    def get(self, request, id_affaire):
        mission_actives = MissionActive.objects.all()

        data = []
        for mission_active in mission_actives:
            affaire = mission_active.id_affaire
            if id_affaire == affaire.id:
                data_mission = mission_active.id_mission
                transform = model_to_dict(data_mission)
                data.append(transform)

        return Response(data)

class GetAllParentMission(APIView):
    def get(self, request):
        data = Mission.objects.filter(mission_parent=None).values()

        return Response(list(data))
    
class GetAllMissionViewByChapitre(APIView):
    def get(self, request, id_affaire):
        missionsActive = MissionActive.objects.filter(id_affaire=id_affaire)
        data = []
        for missionActive in missionsActive:
            # par secu on va prendre les mission sans parent toujours
            mission = missionActive.id_mission
            if mission.mission_parent == None:
                childs = Mission.objects.filter(mission_parent=mission.id)
                if len(childs) == 0:
                    result = {}
                    result['mission'] = model_to_dict(mission)
                    result['chapitre'] = model_to_dict(mission)
                    data.append(result)
                else:
                    for child in childs:
                        result = {}
                        result['mission'] = model_to_dict(mission)
                        result['chapitre'] = model_to_dict(child)
                        data.append(result)
        
        return Response(data)
    

class GetAllArticleForMission(APIView):
    def get(self, request, id_mission, id_affaire):
        articles1 = Article.objects.filter(mission=id_mission, article_parent=None)
        data = []
        for article1 in articles1:
            parentResult1 = {}
            parentResult1['parent'] = model_to_dict(article1)
            parentResult1['childs'] = []
            articles2 = Article.objects.filter(mission=id_mission, article_parent=article1.id)
            for article2 in articles2:
                parentResult2 = {}
                if ArticleSelect.objects.filter(affaire=id_affaire, article=article2.id).exists():
                    parentResult2['parent'] = model_to_dict(article2)
                    parentResult2['childs'] = []
                    articles3 = Article.objects.filter(mission=id_mission, article_parent=article2.id)
                    for article3 in articles3:
                        parentResult3 = {}
                        parentResult3['parent'] = model_to_dict(article3)
                        parentResult3['childs'] = []
                        articles4 = Article.objects.filter(mission=id_mission, article_parent=article3.id)
                        for article4 in articles4:
                            parentResult4 = {}
                            parentResult4['parent'] = model_to_dict(article4)
                            parentResult3['childs'].append(parentResult4)
                        parentResult2['childs'].append(parentResult3)
                    parentResult1['childs'].append(parentResult2)
            if len(parentResult1['childs']) != 0:
                data.append(parentResult1)

        return Response(data)
    
class GetAllCritereForAffaire(APIView):
    def get(self, request, id_affaire):
        articles_mission_active = Article.objects.filter(
            mission__missionactive__id_affaire=id_affaire,
            article_parent__article_parent__isnull=True
        )

        result = []

        for article_mission_active in articles_mission_active:
            if article_mission_active.article_parent != None:
                toAppend = model_to_dict(article_mission_active)
                toAppend['parent'] = model_to_dict(article_mission_active.article_parent)
                check_exist = ArticleSelect.objects.filter(affaire=id_affaire, article=article_mission_active.id).exists()
                toAppend['select'] = check_exist
                result.append(toAppend)

        return Response(result)
    
class AddArticleSelectForAffaire(APIView):
    def get(self, request, id_affaire, id_article):
        exist = ArticleSelect.objects.filter(affaire=id_affaire, article=id_article).exists()

        if not exist:
            new = ArticleSelect(affaire_id=id_affaire, article_id=id_article)
            new.save()
            return Response({'id': new.id})

        return Response({'id': None})
    
class DeleteArticleSelectForAffaire(APIView):
    def get(self, request, id_affaire, id_article):
        try:
            ArticleSelect.objects.filter(affaire=id_affaire, article=id_article).delete()
            return Response({'delete':True})
        except:
            return Response({'delete':False})

class AddMissionActive(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                MissionActive.objects.filter(id_affaire=request.data['affaire']).delete()
                for mission in request.data['missions']:
                    MissionActive(id_affaire_id=request.data['affaire'], id_mission_id=mission).save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
    
class AddInterventionTechnique(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                mission = request.data['mission_sign']
                for collab in request.data['collaborateurs']:
                    if not InterventionTechnique.objects.filter(id_mission_active=mission, id_collaborateur=collab).exists():
                        InterventionTechnique(id_mission_active_id=mission, id_collaborateur_id=collab, affecteur=request.user).save()
        except Exception as ex:
            print(ex)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_201_CREATED)
