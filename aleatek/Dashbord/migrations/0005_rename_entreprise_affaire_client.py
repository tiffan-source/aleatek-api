# Generated by Django 4.2 on 2023-06-01 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0004_planaffaire_libelle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='affaire',
            old_name='entreprise',
            new_name='client',
        ),
    ]
