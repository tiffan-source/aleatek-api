# Generated by Django 4.2 on 2023-06-02 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ouvrage', '0007_rename_constructeur_avis_collaborateurs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affaireouvrage',
            name='statut',
            field=models.CharField(choices=[(0, 'En cours'), (1, 'Accepté'), (2, 'Classé')], default=0, max_length=10),
        ),
    ]
