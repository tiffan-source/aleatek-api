# Generated by Django 4.2 on 2023-06-01 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0010_planaffaire_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='planaffaire',
            name='debut_prestation',
            field=models.DateField(default='2000-12-12'),
            preserve_default=False,
        ),
    ]
