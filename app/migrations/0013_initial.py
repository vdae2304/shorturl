# Generated by Django 4.1.3 on 2022-11-29 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0012_delete_urlmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('shorturl', models.CharField(max_length=10, unique=True)),
                ('creator', models.IntegerField()),
                ('token', models.CharField(max_length=20)),
            ],
        ),
    ]
