from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Produit, PlanAffaire, Affaire, Batiment, Chantier, EntrepriseAffaire
from .permissions import IsAdminAuthenticated
from .serializers import AffaireSerializer, ProduitSerializer, PlanAffaireSerializer, BatimentSerializer, \
    ChantierSerializer, EntrepriseAffaireSerializer
from rest_framework.views import APIView
from adresse.models import Adress
from collaborateurs.models import Collaborateurs
from entreprise.models import Entreprise

from django.forms.models import model_to_dict


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AffaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireSerializer
    queryset = Affaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class PlanAffaireAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = PlanAffaireSerializer
    queryset = PlanAffaire.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ProduitAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProduitSerializer
    queryset = Produit.objects.all()
    permission_classes = [IsAdminAuthenticated]


class BatimentAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = BatimentSerializer
    queryset = Batiment.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ChantierAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ChantierSerializer
    queryset = Chantier.objects.all()
    permission_classes = [IsAdminAuthenticated]

class EntrepriseAffaireViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseAffaireSerializer
    queryset = EntrepriseAffaire.objects.all()
    permission_classes = [IsAdminAuthenticated]



class GetPlanAffaireDetail(APIView):
    def get(self, request):
        planAffaires = PlanAffaire.objects.all().values()
        data = []
        for planAffaire in planAffaires:
            planAffaire_data = dict(planAffaire)
            # On cherche l'affaire
            affaire = Affaire.objects.get(id=planAffaire['affaire_id'])
            planAffaire_data['affaire'] = model_to_dict(affaire)
            # On cherche la ville
            chantier = model_to_dict(Chantier.objects.get(plan_affaire=planAffaire['id']))
            adresse = Adress.objects.get(id=chantier['id'])
            planAffaire_data['ville'] = adresse.ville
            # On cherche le charger
            charger_affaire = Collaborateurs.objects.get(id=model_to_dict(affaire)['charge'])
            planAffaire_data['charge_affaire'] = {
                'nom': charger_affaire.last_name,
                'prenom': charger_affaire.first_name,
            }
            # On cherche le client
            client = Entreprise.objects.get(id=model_to_dict(affaire)['client'])
            planAffaire_data['client'] = client.raison_sociale
            # On cherche le batiment
            batiment = Batiment.objects.get(id=chantier['batiment'])
            planAffaire_data['batiment'] = batiment.libelle

            data.append(planAffaire_data)

        return Response(data)
    
class GetPlanAffaireDetailForPlanAffaire(APIView):
    def get(self, request, id_plan_affaire):
        try:
            planAffaire = PlanAffaire.objects.get(id=id_plan_affaire)

            planAffaire_data = model_to_dict(planAffaire)
            # On cherche l'affaire
            affaire = Affaire.objects.get(id=planAffaire_data['affaire'])
            planAffaire_data['affaire'] = model_to_dict(affaire)
            # On cherche la ville
            chantier = model_to_dict(Chantier.objects.get(plan_affaire=planAffaire_data['id']))
            adresse = Adress.objects.get(id=chantier['id'])
            planAffaire_data['adresse'] = model_to_dict(adresse)
            # On cherche le charger
            charger_affaire = Collaborateurs.objects.get(id=model_to_dict(affaire)['charge'])
            planAffaire_data['charge_affaire'] = model_to_dict(charger_affaire)
            # On cherche le client
            client = Entreprise.objects.get(id=model_to_dict(affaire)['client'])
            adresse_client = client.adresse
            planAffaire_data['client'] = model_to_dict(client)
            planAffaire_data['client']['adresse_detail'] = model_to_dict(adresse_client)
            # On cherche le batiment
            batiment = Batiment.objects.get(id=chantier['batiment'])
            planAffaire_data['batiment'] = batiment.libelle

            return Response(planAffaire_data)
        except:
            return Response({})

class GetAllEntrepriseForAffaire(APIView):
    def get(self, request, id_affaire):
        entreprises = EntrepriseAffaire.objects.filter(affaire=id_affaire)
        data = []
        for entreprise in entreprises:
            data.append(model_to_dict(entreprise.entreprise)['id'])

        return Response(data)


class GetAllEntrepriseDetailForAffaire(APIView):
    def get(self, request, id_affaire):
        entreprises = EntrepriseAffaire.objects.filter(affaire=id_affaire).values()
        data = []
        for entreprise in entreprises:
            final = dict(entreprise)
            detailEntreprise = Entreprise.objects.get(id=entreprise['entreprise_id'])
            final['entreprise'] = model_to_dict(detailEntreprise)
            data.append(final)
        
        return Response(data)

class FindChargeAffaireForAffaire(APIView):
    def get(self, requet, id_affaire):
        try:
            affaire = Affaire.objects.get(id=id_affaire)
            charge = {
                'id' : affaire.charge.id,
                'prenom' : affaire.charge.first_name,
                'nom' : affaire.charge.last_name
            }
            return Response(charge)
        except:
            return Response({"not found" : True})
        
class DeleteEntrepriseAffaire(APIView):
    def get(self, request, id_affaire, id_entreprise):
        # try:
        result = EntrepriseAffaire.objects.get(entreprise=id_entreprise, affaire=id_affaire).delete()
        return Response(result)
        # except:
        #     return Response({})
