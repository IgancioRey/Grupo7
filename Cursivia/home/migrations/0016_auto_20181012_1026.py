# Generated by Django 2.1 on 2018-10-12 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20181011_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]