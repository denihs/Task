# Generated by Django 2.0 on 2018-01-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_remove_perfil_avatar_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
