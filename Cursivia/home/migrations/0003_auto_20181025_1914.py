# Generated by Django 2.1 on 2018-10-25 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_publicacion_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='grupo',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
