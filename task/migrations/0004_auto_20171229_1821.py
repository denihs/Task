# Generated by Django 2.0 on 2017-12-29 21:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20171228_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
