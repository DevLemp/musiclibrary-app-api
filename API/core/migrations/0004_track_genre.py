# Generated by Django 2.1.15 on 2020-02-12 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Genre'),
        ),
    ]
