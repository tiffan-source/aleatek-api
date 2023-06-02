from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer
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
            MissionActive.objects.get(id_mission=id_mission, id_affaire=id_affaire)
            return Response({'check' : True})
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