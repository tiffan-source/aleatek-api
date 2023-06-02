from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Aso, AffaireOuvrage, Avis, Ouvrage, Documents, FichierAttache, EntrepriseAffaireOuvrage, \
    RapportVisite
from .permissions import IsAdminAuthenticated
from .serializers import AsoSerializer, OuvrageSerializer, DocumentSerializer, FichierAttacheSerializer, \
    AvisSerializer, AffaireOuvrageSerializer, EntrepriseAffaireOuvrageSerializer, RapportVisiteSerializer
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from entreprise.models import Entreprise
from Dashbord.models import EntrepriseAffaire


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AsoSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AsoSerializer
    queryset = Aso.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AffaireOuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireOuvrageSerializer
    queryset = AffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class OuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = OuvrageSerializer
    queryset = Ouvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DocumentSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Documents.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AvisSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisSerializer
    queryset = Avis.objects.all()
    permission_classes = [IsAdminAuthenticated]


class FichierSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = FichierAttacheSerializer
    queryset = FichierAttache.objects.all()
    permission_classes = [IsAdminAuthenticated]


class EntrepriseAffaireOuvrageViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseAffaireOuvrageSerializer
    queryset = EntrepriseAffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class VerifyExistAffaireOuvrage(APIView):
    def get(self, request, id_affaire, id_ouvrage):
        try:
            AffaireOuvrage.objects.get(id_affaire=id_affaire, id_ouvrage=id_ouvrage)
            return Response({'check': True})
        except:
            return Response({'check': False})


class GetAllAffaireOuvrageByAffaire(APIView):
    def get(self, request, id_affaire):
        all_affaire_ouvrage = AffaireOuvrage.objects.filter(id_affaire=id_affaire).values()
        data = []
        for ouvrage in all_affaire_ouvrage:
            final_data = dict(ouvrage)  # Convertir l'objet QueryDict en dictionnaire
            detail_ouvrage = Ouvrage.objects.get(id=ouvrage['id_ouvrage_id'])
            ouvrage_data = model_to_dict(detail_ouvrage)
            final_data['ouvrage'] = ouvrage_data
            data.append(final_data)
        return Response(data)


class VerifyEntrepriseCollabOnOuvrage(APIView):
    def get(self, request, id_entreprise_affaire, id_ouvrage_affaire):
        try:
            EntrepriseAffaireOuvrage.objects.get(affaire_ouvrage=id_ouvrage_affaire,
                                                 affaire_entreprise=id_entreprise_affaire)
            return Response({'check': True})
        except:
            return Response({'check': False})


class AllEntreprisebAssignToAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(
            affaire_ouvrage=id_affaire_ouvrage).values()
        data = []
        for e_a_o in entreprise_affaire_ouvrage:
            final = dict(e_a_o)
            detailEntrepriseAffaire = EntrepriseAffaire.objects.get(id=e_a_o['affaire_entreprise_id'])
            detailEntreprise = model_to_dict(detailEntrepriseAffaire.entreprise)
            final['entreprise'] = detailEntreprise
            data.append(final)

        return Response(data)


class RapportVisiteSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = RapportVisiteSerializer
    queryset = RapportVisite.objects.all()
    permission_classes = [IsAdminAuthenticated]


class RecupereLensembleDesAvisSurDocument(APIView):
    def get(self, request, affaire_ouvrage_id):
        aviss = Avis.objects.all()
        TabCodifications = []
        for avis in aviss:
            document = avis.id_document
            entreprise_affaire_ouvrage = document.emetteur
            affaire_ouvrage = entreprise_affaire_ouvrage.affaire_ouvrage
            print(affaire_ouvrage.id)
            if affaire_ouvrage.id == affaire_ouvrage_id:
                TabCodifications.append(avis.codification)
        return Response(TabCodifications)

class GetAllDetailDocument(APIView):
    def get(self, request, id_affaire):
        all_document = Documents.objects.all()

        data = []

        for document in all_document:
            emetteur = document.emetteur
            if emetteur != None:
                affaireOuvrage = emetteur.affaire_ouvrage
                affaireEntreprise = emetteur.affaire_entreprise

                id = affaireOuvrage.id_affaire.id
                if id == id_affaire:
                    prepare = model_to_dict(document)
                    ouvrage = affaireOuvrage.id_ouvrage
                    print(ouvrage)
                    entreprise = affaireEntreprise.entreprise

                    prepare['ouvrage'] = model_to_dict(ouvrage)
                    prepare['entreprise'] = model_to_dict(entreprise)

                    data.append(prepare)

        return Response(data)
    
class GetAllDetailDocumentWithIdDoc(APIView):
    def get(self, request, id_affaire, id_doc):
        all_document = Documents.objects.all()
        data = []

        for document in all_document:
            emetteur = document.emetteur
            if emetteur is not None:
                affaireOuvrage = emetteur.affaire_ouvrage
                affaireEntreprise = emetteur.affaire_entreprise

                id = affaireOuvrage.id_affaire.id
                if id == id_affaire:
                    prepare = model_to_dict(document)
                    ouvrage = affaireOuvrage.id_ouvrage
                    entreprise = affaireEntreprise.entreprise

                    prepare['ouvrage'] = model_to_dict(ouvrage)
                    prepare['entreprise'] = model_to_dict(entreprise)

                    data.append(prepare)

        if id_doc is not None:
            filtered_data = [doc for doc in data if doc['id'] == id_doc]
            if len(filtered_data) == 0:
                return Response({'error': 'Document not found'}, status=404)
            return Response(filtered_data[0])
        
        return Response(data)


class CheckAvisOnDocumentByCollaborateur(APIView):
    def get(self, request, id_document, id_collaborateur):
        all_avis = Avis.objects.all()
        find = None
        for avis in all_avis:
            document = avis.id_document
            collab = avis.collaborateurs
            if document.id == id_document and collab.id == id_collaborateur:
                find = avis
                break

        if find == None:
            return Response({'avis' : False})
        else:
            return Response({'avis' : model_to_dict(find)})
        