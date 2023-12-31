# Generated by Django 3.2.12 on 2023-08-01 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RICT', '0010_commentaireavisarticle_lever'),
        ('commentaire', '0005_commentaire_lever'),
        ('rapport_visite', '0011_commentaireavisouvrage_lever'),
        ('synthese', '0003_alter_syntheseavis_statut'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyntheseCommentaireDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commentaire.commentaire')),
                ('synthese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='synthese.syntheseavis')),
            ],
        ),
        migrations.CreateModel(
            name='SyntheseCommentaireArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RICT.commentaireavisarticle')),
                ('synthese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='synthese.syntheseavis')),
            ],
        ),
        migrations.CreateModel(
            name='SyntheseComentaireRV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapport_visite.commentaireavisouvrage')),
                ('synthese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='synthese.syntheseavis')),
            ],
        ),
    ]
