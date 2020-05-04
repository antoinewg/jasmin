# Generated by Django 3.0.5 on 2020-05-03 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equities', '0002_auto_20200503_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gap',
            old_name='next_open',
            new_name='open',
        ),
        migrations.RenameField(
            model_name='gap',
            old_name='close',
            new_name='prev_close',
        ),
        migrations.AddField(
            model_name='gap',
            name='ascending',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]