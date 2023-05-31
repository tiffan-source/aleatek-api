from django.db import models

from Dashbord.models import Affaire

from collaborateurs.models import Collaborateurs


# Create your models here.

class Mission(models.Model):
    code_mission = models.CharField(max_length=10)
    libelle = models.CharField(max_length=100)


class MissionActive(models.Model):
    id_mission = models.OneToOneField(Mission, on_delete=models.CASCADE)
    id_affaire = models.OneToOneField(Affaire, on_delete=models.CASCADE)


class InterventionTechnique(models.Model):
    id_mission_active = models.OneToOneField(MissionActive, on_delete=models.CASCADE)
    id_collaborateur = models.OneToOneField(Collaborateurs, on_delete=models.CASCADE)
