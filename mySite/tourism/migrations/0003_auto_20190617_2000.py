# Generated by Django 2.2 on 2019-06-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0002_userinfo_tree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(),
        ),
    ]
