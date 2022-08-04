# Generated by Django 3.0.14 on 2022-07-23 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_company_e_waste'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='update',
            name='employee_name',
            field=models.CharField(default='Roocha', max_length=200),
        ),
    ]
