# Generated by Django 4.2 on 2023-06-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0009_planaffaire_type_montant'),
    ]

    operations = [
        migrations.AddField(
            model_name='planaffaire',
            name='doc',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]