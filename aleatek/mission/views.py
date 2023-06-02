from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Mission, MissionActive, InterventionTechnique
from .permissions import IsAdminAuthenticated
from .serializers import MissionSerializer, MissionActiveSerializer, InterventionTechniqueSerializer
from rest_framework.views import APIView
from Dashbord.models import Affaire, PlanAffaire
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
        