from django.db import models

from Dashbord.models import Affaire, EntrepriseAffaire
from collaborateurs.models import Collaborateurs
from django.db.models import UniqueConstraint


class Ouvrage(models.Model):
    libelle = models.CharField(max_length=200)


class AffaireOuvrage(models.Model):
    id_affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)
    id_ouvrage = models.ForeignKey(Ouvrage, on_delete=models.CASCADE)
    validateur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, null=True)


class Aso(models.Model):
    ETAPES = [
        (0, 'En cours'),
        (1, 'Accepté'),
        (2, 'Classé'),
        (3, 'Diffuse'),
    ]
    date = models.DateField()
    statut = models.CharField(max_length=10, choices=ETAPES, default=0)
    redacteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, null=True)
    affaireouvrage = models.ForeignKey(AffaireOuvrage, on_delete=models.CASCADE)


class EntrepriseAffaireOuvrage(models.Model):
    affaire_ouvrage = models.ForeignKey(AffaireOuvrage, on_delete=models.CASCADE)
    affaire_entreprise = models.ForeignKey(EntrepriseAffaire, on_delete=models.CASCADE)
    diffusion = models.BooleanField(default=False)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['affaire_ouvrage', 'affaire_entreprise'], name='unique_entreprise_ouvrage')
        ]

class Documents(models.Model):
    Nature = [
        ('TOUS', 'TOUS'),
        ('Descriptif', 'Descriptif'),
        ('AT/DTA', 'AT/DTA'),
        ('Attestation Incendie', 'Attestation Incendie'),
        ('Carnet', 'Carnet'),
        ('Certificat', 'Certificat'),
        ('Certificat incendie', 'Certificat incendie'),
        ('Compte rendue', 'Compte rendu'),
        ('Courrier', 'Courrier'),
        ('fiche techinique', 'Fiche Technique'),
        ('Note', 'Note'),
        ('Note de calcule', 'Note de calcule'),
        ('Notice', 'Notice'),
        ('Plan', 'Plan'),
        ('PV', 'PV'),
        ('PV Incendie', 'PV Incendie'),
        ('Rapport', 'Rapport'),
        ('Schéma', 'Schéma')
    ]
    dossier = models.CharField(max_length=200, default='Execution', choices=(('Execution', 'Execution'),
                                                                             ('Conception', 'Conception')))
    nature = models.CharField(choices=Nature, max_length=30)
    indice = models.CharField(max_length=5)
    date_indice = models.DateField()
    date_reception = models.DateField()
    titre = models.CharField(max_length=100)
    numero_revision = models.IntegerField()
    numero_externe = models.IntegerField(blank=True, null=True)
    emetteur = models.ForeignKey(EntrepriseAffaireOuvrage, on_delete=models.CASCADE, null=True)
    aso = models.ForeignKey(Aso, on_delete=models.SET_NULL, null=True)


class FichierAttache(models.Model):
    nom = models.CharField(max_length=250)
    fichier = models.FileField(upload_to='fichierattachedocument')
    date = models.DateField()
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_fichier


class Avis(models.Model):
    AVIS = [
        ('F', 'F'),
        ('RMQ', 'RMQ'),
        ('FA', 'FA'),
        ('HM', 'HM'),
        ('SO', 'SO'),
        ('VI', 'VI')]
    id_document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    codification = models.CharField(max_length=23, choices=AVIS)
    collaborateurs = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE)
