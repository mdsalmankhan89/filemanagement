# Generated by Django 2.0.4 on 2020-04-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='create_dte',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]