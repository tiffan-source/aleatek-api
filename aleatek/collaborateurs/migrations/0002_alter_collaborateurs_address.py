# Generated by Django 4.2 on 2023-05-31 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adresse', '0001_initial'),
        ('collaborateurs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='address',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='adresse.adress'),
        ),
    ]
