from django.db import models
from Dashbord.models import Affaire
from collaborateurs.models import Collaborateurs
from ouvrage.models import AffaireOuvrage
# Create your models here.

class RapportVisite(models.Model):
    date = models.DateField()
    redacteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    objet = models.CharField(max_length=20)

class AvisOuvrage(models.Model):
    ouvrage = models.ForeignKey(AffaireOuvrage, on_delete=models.CASCADE)
    objet = models.CharField(max_length=200)

class CommentaireAvisOuvrage(models.Model):
    asuivre = models.BooleanField(default=False),
    commentaire = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    avis = models.ForeignKey(AvisOuvrage, on_delete=models.CASCADE)