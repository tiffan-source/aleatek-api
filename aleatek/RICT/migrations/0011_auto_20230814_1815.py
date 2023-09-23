# Generated by Django 3.2.12 on 2023-08-14 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0009_auto_20230814_1815'),
        ('RICT', '0010_commentaireavisarticle_lever'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisarticle',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.articleselect'),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.articleselect'),
        ),
    ]