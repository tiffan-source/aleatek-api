from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Collaborateurs
from .permissions import IsAdminAuthenticated
from .serializers import ColaboratteursSerializer
from rest_framework.views import APIView
from mission.models import InterventionTechnique
from django.forms.models import model_to_dict

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CollaborateursAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ColaboratteursSerializer
    queryset = Collaborateurs.objects.all()
    permission_classes = [IsAdminAuthenticated]


class UtilisateurConnecteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id
        }
        return Response(data)
    
class AllCollabAssignToMission(APIView):
    def get(self, request, id_mission_sign):
        collab_data_to_retrieve = InterventionTechnique.objects.filter(id_mission_active=id_mission_sign).values()
        data = []
        for collab in collab_data_to_retrieve:
            collab_data = dict(collab)
            # On cherche le collaborateur
            collab = Collaborateurs.objects.get(id=collab_data['id_collaborateur_id'])
            collab_data['collaborateur'] = {
                'nom' : collab.last_name,
                'prenom' : collab.first_name,
            }
            data.append(collab_data)

        return Response(data)

