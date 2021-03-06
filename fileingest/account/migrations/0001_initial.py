# Generated by Django 2.0.4 on 2020-04-27 08:18

import account.storage
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.CharField(max_length=250)),
                ('logs', models.CharField(default='TEST1', max_length=250)),
                ('create_dte', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('uploadid', models.AutoField(primary_key=True, serialize=False)),
                ('files', models.FileField(storage=account.storage.CustomFileSystemStorage(), upload_to='files/')),
                ('create_dte', models.DateTimeField(default=datetime.datetime.now)),
                ('isactive', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FilesData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filelabel', models.CharField(max_length=255, null=True)),
                ('userid', models.IntegerField()),
                ('ruleid', models.IntegerField()),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('ruleid', models.AutoField(primary_key=True, serialize=False)),
                ('rule', models.TextField()),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='filelogs',
            name='uploadid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upload_id', to='account.Files'),
        ),
    ]
