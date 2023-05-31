from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Responsable, Entreprise


class ResponsableSerializer(ModelSerializer):
    class Meta:
        model = Responsable
        exclude = ['password']

    def validate_mail(self, value):
        # Nous vérifions que la le libelle  existe
        if Responsable.objects.filter(email=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Cette mail  existe déjà Existe déja')
        return value
