# Generated by Django 2.0 on 2018-08-16 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Essay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='essay',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
