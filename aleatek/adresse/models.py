from django.db import models


# Create your models here.

class Adress(models.Model):
    cplt_geo = models.CharField(max_length=250)
    numero_voie = models.CharField(max_length=500)
    lieu_dit = models.CharField(max_length=250)
    compte_postal = models.CharField(max_length=5, blank=True)
    ville = models.CharField(max_length=500)
    pays = models.CharField(max_length=500, default='France')
    departement = models.CharField(max_length=500, default='Mompellier')
    province = models.CharField(max_length=500)
