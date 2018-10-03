# Generated by Django 2.1 on 2018-09-26 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20180925_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default='', max_length=50)),
                ('año', models.IntegerField(default=0)),
                ('carrera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Carrera')),
            ],
        ),
        migrations.AddField(
            model_name='publicacion',
            name='alcance',
            field=models.CharField(blank=True, choices=[('g', 'Globla'), ('e', 'Expeficifico')], default='g', help_text='alcance de la publicacion', max_length=1),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='estado_comentario',
            field=models.CharField(blank=True, choices=[('p', 'Publicado'), ('b', 'Borrador'), ('d', 'Denunciado'), ('e', 'Eliminado')], default='b', help_text='situacion actual del comentario', max_length=1),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='estado_publicacion',
            field=models.CharField(blank=True, choices=[('p', 'Publicado'), ('b', 'Borrador'), ('d', 'Denunciado'), ('e', 'Eliminado')], default='b', help_text='situacion actual de la publicacion', max_length=1),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='tipo_publicacion',
            field=models.CharField(blank=True, choices=[('n', 'Noticia'), ('d', 'Documentacion')], default='d', help_text='situacion actual de la publicacion', max_length=1),
        ),
        migrations.DeleteModel(
            name='EstadoPublicacion',
        ),
        migrations.DeleteModel(
            name='TipoPublicacion',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='Materia',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.Materia'),
            preserve_default=False,
        ),
    ]
