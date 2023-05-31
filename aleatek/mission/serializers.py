from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MissionActive, Mission, InterventionTechnique


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class MissionActiveSerializer(ModelSerializer):
    class Meta:
        model = MissionActive
        fields = '__all__'


class InterventionTechniqueSerializer(ModelSerializer):
    class Meta:
        model = InterventionTechnique
        fields = '__all__'
