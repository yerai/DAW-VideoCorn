# Generated by Django 2.0.4 on 2018-04-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videocorn', '0002_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.CharField(help_text='Introduzca la valoración', max_length=1)),
            ],
        ),
    ]