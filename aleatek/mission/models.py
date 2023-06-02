from django.db import models

from Dashbord.models import Affaire

from collaborateurs.models import Collaborateurs


# Create your models here.

class Mission(models.Model):
    code_mission = models.CharField(max_length=10)
    libelle = models.CharField(max_length=100)


class MissionActive(models.Model):
    id_mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    id_affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)


class InterventionTechnique(models.Model):
    affecteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, related_name='ITAffecteur')
    date = models.DateField()
    id_mission_active = models.ForeignKey(MissionActive, on_delete=models.CASCADE)
    id_collaborateur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, related_name='ITAffecter')
