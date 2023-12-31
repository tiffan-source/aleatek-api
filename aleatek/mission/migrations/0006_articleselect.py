# Generated by Django 3.2.19 on 2023-06-19 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0026_auto_20230618_1622'),
        ('mission', '0005_alter_mission_mission_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSelect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affaire_article_select', to='Dashbord.affaire')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_article_select', to='mission.article')),
            ],
        ),
    ]
