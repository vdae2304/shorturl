# Generated by Django 4.1.3 on 2022-11-29 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_urlmodel_creator_alter_urlmodel_token'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='URLModel',
            new_name='URLModels',
        ),
    ]
