# Generated by Django 3.0.14 on 2022-07-18 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20220715_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='date_of_activity',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='update',
            name='recycling_percentage',
            field=models.IntegerField(default=100, null=True),
        ),
    ]