# Generated by Django 4.2 on 2023-06-01 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adresse', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adress',
            old_name='compte_postal',
            new_name='code_postal',
        ),
    ]