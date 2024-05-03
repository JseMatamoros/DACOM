# Generated by Django 5.0.4 on 2024-04-13 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuesta',
            name='preguntas_encuesta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='encuestas.pregunta'),
        ),
    ]