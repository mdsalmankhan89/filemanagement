# Generated by Django 3.0.4 on 2020-04-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('ruleid', models.AutoField(primary_key=True, serialize=False)),
                ('rule', models.TextField()),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
    ]
