# Generated by Django 2.0.7 on 2018-07-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='vierws',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
