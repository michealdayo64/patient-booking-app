# Generated by Django 4.2 on 2023-06-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_alter_account_id_additionalinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalinformation',
            name='my_insure_carrier',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
