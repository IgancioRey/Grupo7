# Generated by Django 2.1 on 2018-09-25 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cometario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=200)),
                ('fechaHora', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('fecha_baja', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=80)),
                ('cuerpo', models.CharField(max_length=1000)),
                ('fecha_alta', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('fecha_baja', models.DateTimeField(null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cometario',
            name='publicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Publicacion'),
        ),
        migrations.AddField(
            model_name='cometario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
