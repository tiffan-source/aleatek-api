# Generated by Django 4.2 on 2023-06-02 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ouvrage', '0006_rename_cree_le_fichierattache_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avis',
            old_name='constructeur',
            new_name='collaborateurs',
        ),
    ]
