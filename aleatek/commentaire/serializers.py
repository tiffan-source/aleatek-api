from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import commentaire


class CommentaireSerializer(ModelSerializer):
    class Meta:
        model = commentaire
        fields = '__all__'

