# Generated by Django 3.2.19 on 2023-06-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapport_visite', '0002_auto_20230614_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaireavisouvrage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
