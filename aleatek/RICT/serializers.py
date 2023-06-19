from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import RICT, Disposition, AvisArticle, CommentaireAvisArticle


class RICTSerializer(ModelSerializer):
    class Meta:
        model = RICT
        fields = '__all__'
    
class DispositionSerializer(ModelSerializer):
    class Meta:
        model = Disposition
        fields = '__all__'

class AvisArticleSerializer(ModelSerializer):
    class Meta:
        model = AvisArticle
        fields = '__all__'

class CommentaireAvisArticleSerializer(ModelSerializer):
    class Meta:
        model = CommentaireAvisArticle
        fields = '__all__'