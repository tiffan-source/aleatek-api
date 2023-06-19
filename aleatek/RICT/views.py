from django.shortcuts import render
from .permissions import IsAdminAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import RICTSerializer, DispositionSerializer, AvisArticleSerializer, CommentaireAvisArticleSerializer
from .models import RICT, Disposition, AvisArticle, CommentaireAvisArticle
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict

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


class CheckRICTForAffaire(APIView):
    def get(self, request, id_affaire):
        try:
            rict = RICT.objects.get(affaire=id_affaire)
            return Response(model_to_dict(rict))
        except:
            return Response(False)