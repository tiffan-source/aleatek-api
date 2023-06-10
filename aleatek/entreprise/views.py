from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Responsable, Entreprise
from .permissions import IsAdminAuthenticated
from .serializers import ResponsableSerializer
from rest_framework.views import APIView
from adresse.models import Adress
from django.forms.models import model_to_dict

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ResponsableAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ResponsableSerializer
    queryset = Responsable.objects.all()
    permission_classes = [IsAdminAuthenticated]


from .serializers import EntrepriseSerializer


class EntrepriseAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseSerializer
    queryset = Entreprise.objects.all()
    permission_classes = [IsAdminAuthenticated]

class GetEntrepriseWithCollaborateur(APIView):
    def get(self, request, id_entreprise=None):
        if id_entreprise is not None:
            entreprise = Entreprise.objects.filter(id=id_entreprise).values().first()
            if entreprise is None:
                return Response({'message': 'Entreprise non trouvée'}, status=status.HTTP_404_NOT_FOUND)
            
            entreprise_data = {
                'id': entreprise['id'],
                'raison_sociale': entreprise['raison_sociale'],
                'siret': entreprise['siret'],
                'activite': entreprise['activite'],
                'adresse': {}
            }
            adresse = Adress.objects.get(id=entreprise['adresse_id'])
            entreprise_data['adresse'] = model_to_dict(adresse)
            responsables = Responsable.objects.filter(entreprise_id=entreprise['id'])
            entreprise_data['responsables'] = []
            for responsable in responsables:
                entreprise_data['responsables'].append(model_to_dict(responsable))
            
            return Response(entreprise_data)
        
        else:
            entreprises = Entreprise.objects.all().values()
            data = []
            for entreprise in entreprises:
                entreprise_data = {
                    'id': entreprise['id'],
                    'raison_sociale': entreprise['raison_sociale'],
                    'siret': entreprise['siret'],
                    'activite': entreprise['activite'],
                    'adresse': {}
                }
                adresse = Adress.objects.get(id=entreprise['adresse_id'])
                entreprise_data['adresse'] = model_to_dict(adresse)
                responsables = Responsable.objects.filter(entreprise_id=entreprise['id'])
                entreprise_data['responsables'] = []
                for responsable in responsables:
                    entreprise_data['responsables'].append(model_to_dict(responsable))
                data.append(entreprise_data)

            return Response(data)
