# Generated by Django 4.2.1 on 2023-05-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_policeuser_adminposition'),
    ]

    operations = [
        migrations.CreateModel(
            name='replay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.CharField(default='', max_length=30)),
                ('replay', models.TextField(default='')),
            ],
        ),
    ]