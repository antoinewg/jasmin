# Generated by Django 3.0.5 on 2020-05-03 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equities', '0003_auto_20200503_2053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gap',
            old_name='next_volume',
            new_name='volume',
        ),
    ]
