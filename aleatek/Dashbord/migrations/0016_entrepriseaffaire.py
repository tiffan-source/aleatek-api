# Generated by Django 4.2 on 2023-06-01 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entreprise', '0004_rename_responsable_responsable_entreprise'),
        ('Dashbord', '0015_remove_planaffaire_reunions'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntrepriseAffaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord.affaire')),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprise.entreprise')),
            ],
        ),
    ]
