# Generated by Django 4.2 on 2023-05-31 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprise', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entreprise',
            name='raison_sociale',
        ),
        migrations.AddField(
            model_name='entreprise',
            name='nom',
            field=models.CharField(default='', max_length=100, verbose_name='Raison sociale'),
            preserve_default=False,
        ),
    ]
