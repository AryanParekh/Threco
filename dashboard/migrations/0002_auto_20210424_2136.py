# Generated by Django 3.1.7 on 2021-04-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='carbon_emission_saved',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]