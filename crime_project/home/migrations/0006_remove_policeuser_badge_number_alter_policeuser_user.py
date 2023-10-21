# Generated by Django 4.2.1 on 2023-05-16 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_policeuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policeuser',
            name='badge_number',
        ),
        migrations.AlterField(
            model_name='policeuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]