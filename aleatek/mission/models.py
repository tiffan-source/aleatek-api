from django.db import models

from Dashbord.models import Affaire

from collaborateurs.models import Collaborateurs


# Create your models here.

class Mission(models.Model):
    code_mission = models.CharField(max_length=10)
    libelle = models.CharField(max_length=100)
    mission_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sous_missions', limit_choices_to={'mission_parent__isnull': True})

    def __str__(self):
        return self.code_mission


class MissionActive(models.Model):
    id_mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    id_affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE)


class InterventionTechnique(models.Model):
    affecteur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, related_name='ITAffecteur')
    date = models.DateField()
    id_mission_active = models.ForeignKey(MissionActive, on_delete=models.CASCADE)
    id_collaborateur = models.ForeignKey(Collaborateurs, on_delete=models.CASCADE, related_name='ITAffecter')


class Article(models.Model):
    titre = models.CharField(max_length=500)
    article_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sous_articles')
    commentaire = models.TextField(blank=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='articles')

    def save(self, *args, **kwargs):
        if self.article_parent:
            if self.mission != self.article_parent.mission:
                raise ValueError("La mission de l'article doit correspondre à la mission de son article parent.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

class ArticleSelect(models.Model):
    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE, related_name='affaire_article_select')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_article_select')