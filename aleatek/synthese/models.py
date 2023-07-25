from django.db import models
from Dashbord.models import Affaire
from collaborateurs.models import Collaborateurs
import datetime
# Create your models here.

class SyntheseAvis(models.Model):
    ETAPES = [
        (0, 'En cours'),
        (1, 'Accepté'),
        (2, 'Classé'),
        (3, 'Diffuse'),
    ]
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    createur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    date = models.DateField(blank=True, default=datetime.date.today)
    statut = models.IntegerField(choices=ETAPES, default=0)
    order = models.IntegerField(default=0)
