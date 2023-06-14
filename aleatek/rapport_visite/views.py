from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import RapportVisiteSerializer, AvisOuvrageSerializer, CommentaireAvisOuvrageSerializer
from .models import RapportVisite, AvisOuvrage, CommentaireAvisOuvrage
from .permissions import IsAdminAuthenticated
# Create your views here.
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from rest_framework.response import Response
from ouvrage.models import EntrepriseAffaireOuvrage, AffaireOuvrage
from mission.models import MissionActive
from entreprise.models import Responsable

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class RapportVisiteSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = RapportVisiteSerializer
    queryset = RapportVisite.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AvisOuvrageViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisOuvrageSerializer
    queryset = AvisOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]

class CommentaireAvisOuvrageViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentaireAvisOuvrageSerializer
    queryset = CommentaireAvisOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class GetAllRapportVisiteByAffaire(APIView):
    def get(self, request, affaire):
        all_avis = RapportVisite.objects.filter(affaire=affaire)
        data = []
        for avis in all_avis:
            pre = model_to_dict(avis)
            data.append(pre)

        return Response(data)
    
class GetAllRapportVisiteOneVersions(APIView):
    def get(self, request, rv):
        rapportVisite = RapportVisite.objects.get(id=rv)
        pre = model_to_dict(rapportVisite)

        return Response(pre)
    
class AllEntrepriseConcerneByRV(APIView):
    def get(self, request, id_rv):
        all_avis = AvisOuvrage.objects.filter(rv=id_rv)
        data = []
        for avis in all_avis:
            all_entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=avis.ouvrage)
            for entreprise_affaire_ouvrage in all_entreprise_affaire_ouvrage:
                result = model_to_dict(entreprise_affaire_ouvrage)
                result['detail_entreprise'] = model_to_dict(entreprise_affaire_ouvrage.affaire_entreprise.entreprise)
                result['responsables'] = []
                responsables = Responsable.objects.filter(entreprise=entreprise_affaire_ouvrage.affaire_entreprise.entreprise.id)
                for responsable in responsables:
                    result['responsables'].append(model_to_dict(responsable))
                data.append(result)

        return Response(data)
    
class GenerateDataForRV(APIView):
    def get(self, request, id_rv):
        # try:
            rv = RapportVisite.objects.get(id=id_rv)

            data = {}

            data['rv'] = model_to_dict(rv)

            data['affaire'] = model_to_dict(rv.affaire)

            charge = rv.affaire.charge

            data['charge'] = model_to_dict(charge)
            data['charge']['adresse'] = model_to_dict(charge.address)

            entreprise = rv.affaire.client

            data['client'] = model_to_dict(entreprise)
            data['client']['adresse'] = model_to_dict(entreprise.adresse)


            data['mission'] = []
            id_affaire = rv.affaire.id

            all_mission = MissionActive.objects.filter(id_affaire=id_affaire)

            for mission in all_mission:
                data['mission'].append(model_to_dict(mission.id_mission))

            data['ouvrages'] = []

            ouvrages = AffaireOuvrage.objects.all()
            for ouvrage in ouvrages:
                all_avis_for_ouvrage = AvisOuvrage.objects.filter(ouvrage=ouvrage.id, rv=id_rv)
                if len(all_avis_for_ouvrage) != 0:
                    result = model_to_dict(ouvrage.id_ouvrage)
                    result['all_avis'] = []
                    for avis in all_avis_for_ouvrage:
                        subresult = model_to_dict(avis)
                        subresult['comments'] = []
                        all_comment = CommentaireAvisOuvrage.objects.filter(avis=avis.id)
                        for comment in all_comment:
                            pre = {
                                'asuivre': 1 if comment.asuivre else 0,
                                'commentaire': comment.commentaire,
                                'image': comment.image.url if comment.image else None,
                                'avis': comment.avis_id
                            }
                            # print(str(pre['image']))
                            # if str(pre['image']) == "":
                            #     del pre['image']
                            subresult['comments'].append(pre)

                        result['all_avis'].append(subresult)
                    data['ouvrages'].append(result)


            return Response(data)
        # except:
        #     return Response({})