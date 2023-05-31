from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Responsable, Entreprise


class ResponsableSerializer(ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'


class EntrepriseSerializer(ModelSerializer):
    class Meta:
        model = Responsable
        fields = '__all__'
