# Generated by Django 4.2 on 2023-06-02 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ouvrage', '0008_alter_affaireouvrage_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aso',
            name='redacteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
