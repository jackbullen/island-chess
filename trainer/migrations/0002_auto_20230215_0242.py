# Generated by Django 3.1.3 on 2023-02-15 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='fen',
            field=models.TextField(max_length=100),
        ),
    ]