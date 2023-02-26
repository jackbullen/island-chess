# Generated by Django 3.1.3 on 2023-02-14 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Repertoire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('fen', models.CharField(max_length=100)),
                ('pgn', models.TextField()),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.line')),
            ],
        ),
        migrations.CreateModel(
            name='Opening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('eco', models.CharField(max_length=6)),
                ('repertoire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.repertoire')),
            ],
        ),
        migrations.AddField(
            model_name='line',
            name='opening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.opening'),
        ),
    ]