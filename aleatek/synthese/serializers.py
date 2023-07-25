from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import SyntheseAvis

class SyntheseAvisSerializer(ModelSerializer):
    class Meta:
        model = SyntheseAvis
        fields = '__all__'