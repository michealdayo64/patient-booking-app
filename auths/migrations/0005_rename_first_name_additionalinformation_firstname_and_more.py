# Generated by Django 4.2 on 2023-06-06 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0004_remove_additionalinformation_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='additionalinformation',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='additionalinformation',
            old_name='lastname_name',
            new_name='lastname',
        ),
    ]
