# Generated by Django 3.2 on 2024-02-19 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20240218_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-id']},
        ),
    ]
