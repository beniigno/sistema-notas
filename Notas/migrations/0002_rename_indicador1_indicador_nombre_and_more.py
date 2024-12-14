# Generated by Django 5.1.3 on 2024-12-04 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicador',
            old_name='indicador1',
            new_name='nombre',
        ),
        migrations.RemoveField(
            model_name='indicador',
            name='indicador2',
        ),
        migrations.RemoveField(
            model_name='indicador',
            name='indicador3',
        ),
        migrations.RemoveField(
            model_name='indicador',
            name='indicador4',
        ),
        migrations.RemoveField(
            model_name='indicador',
            name='indicador5',
        ),
        migrations.AddField(
            model_name='indicador',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='CursoIndicador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notas.curso')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notas.docente')),
                ('indicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notas.indicador')),
            ],
        ),
    ]