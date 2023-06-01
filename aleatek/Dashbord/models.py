from django.db import models

from adresse.models import Adress
from entreprise.models import Entreprise


# Create your models here.

class Produit(models.Model):
    code_produit = models.CharField(max_length=3)
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.code_produit


class Batiment(models.Model):
    libelle = models.CharField(max_length=50)


class Affaire(models.Model):
    STATUS = [
        ('En cours', 'En cours'),
        ('Achevé', 'Achevé'),
        ('Abandonné', 'Abandonné')
    ]
    numero = models.IntegerField()
    libelle = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUS)
    numero_offre = models.IntegerField()
    numero_contrat = models.IntegerField
    libelle_contrat = models.CharField(max_length=100)
    date_contrat = models.DateField()
    client = models.ForeignKey(Entreprise, on_delete=models.CASCADE)

class PlanAffaire(models.Model):
    RISQUES = [
        ('Normal', 'Normal'),
        ('Particulier', 'Particulier'),
        ('Complexe', 'Complexe')

    ]
    DEVISE = [
        ('$', '$'),
        ('€', '€')
    ]

    TYPES_AFFAIRES = [
        ('CTC', 'CTC'),
        ('VT', 'VT')
    ]
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    numero = models.IntegerField()
    risque = models.CharField(max_length=20, choices=RISQUES)
    libelle = models.CharField(max_length=50)
    devise = models.CharField(max_length=10, choices=DEVISE)
    type = models.CharField(max_length=10, choices=TYPES_AFFAIRES)
    prix = models.IntegerField()
    debut_chantier = models.DateField()
    fin_chantier = models.DateField()
    reunions = models.IntegerField()
    visite = models.IntegerField()

class Chantier(models.Model):
    batiment = models.OneToOneField(Batiment, on_delete=models.CASCADE)
    plan_affaire = models.OneToOneField(PlanAffaire, on_delete=models.CASCADE)
    adresse = models.OneToOneField(Adress, models.CASCADE)

