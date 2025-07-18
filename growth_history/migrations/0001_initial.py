# Generated by Django 5.2.4 on 2025-07-12 14:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowthHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_evento', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_evento', models.CharField(help_text='Ex: Mudança de Estágio, Poda, Foto, Observação', max_length=100)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='growth_history/')),
                ('observacoes', models.TextField()),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico', to='plants.plant')),
            ],
            options={
                'ordering': ['-data_hora_evento'],
            },
        ),
    ]
