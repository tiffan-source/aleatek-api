from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Aso, AffaireOuvrage, Avis, Ouvrage, Documents, FichierAttache


class AsoSerializer(ModelSerializer):
    class Meta:
        model = Aso
        fields = '__all__'


class AffaireOuvrageSerializer(ModelSerializer):
    class Meta:
        model = AffaireOuvrage
        fields = '__all__'


class AvisSerializer(ModelSerializer):
    class Meta:
        model = Avis
        fields = '__all__'


class OuvrageSerializer(ModelSerializer):
    class Meta:
        model = Ouvrage
        fields = '__all__'


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class FichierAttacheSerializer(ModelSerializer):
    class Meta:
        model = FichierAttache
        fields = '__all__'


