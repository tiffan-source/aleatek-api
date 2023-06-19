from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique, Article
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer, ArticleSerializer
from rest_framework.views import APIView
from Dashbord.models import Affaire, PlanAffaire
from collaborateurs.models import Collaborateurs
from django.forms.models import model_to_dict


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

class MissionActiveAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = MissionActiveSerializer
    queryset = MissionActive.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ITAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = InterventionTechniqueSerializer
    queryset = InterventionTechnique.objects.all()
    permission_classes = [IsAdminAuthenticated]

class MissionActiveForCurrentAffaire(APIView):
    def get(self, request, id_plan):
        plan_aff = PlanAffaire.objects.get(id=id_plan)

        all_mission_active = MissionActive.objects.filter(id_affaire=plan_aff.affaire).values()

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
    def get(self, request, id_mission):
        articles1 = Article.objects.filter(mission=id_mission, article_parent=None)
        data = []
        for article1 in articles1:
            parentResult1 = {}
            parentResult1['parent'] = model_to_dict(article1)
            parentResult1['childs'] = []
            articles2 = Article.objects.filter(mission=id_mission, article_parent=article1.id)
            for article2 in articles2:
                parentResult2 = {}
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
            data.append(parentResult1)

        return Response(data)


