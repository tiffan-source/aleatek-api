# Generated by Django 3.2.12 on 2023-07-19 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('synthese', '0003_alter_syntheseavis_statut'),
        ('RICT', '0007_descriptionsommaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaireavisarticle',
            name='synthese',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='synthese.syntheseavis'),
        ),
    ]
