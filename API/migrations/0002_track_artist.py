# Generated by Django 2.1.13 on 2020-01-29 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='artist',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]