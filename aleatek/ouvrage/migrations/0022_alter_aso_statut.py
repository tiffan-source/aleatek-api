# Generated by Django 3.2.19 on 2023-06-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ouvrage', '0021_remove_documents_valider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aso',
            name='statut',
            field=models.CharField(choices=[(0, 'En cours'), (1, 'Accepté'), (2, 'Classé'), (3, 'Diffuse')], default=0, max_length=10, null=True),
        ),
    ]
