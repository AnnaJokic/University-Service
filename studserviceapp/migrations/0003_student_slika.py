# Generated by Django 2.2.3 on 2019-07-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studserviceapp', '0002_izborgrupe_izbornagrupa_konsultacije_obavestenje_rasporedpolaganja_terminpolaganja_vaznidatumi'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='slika',
            field=models.ImageField(default=None, upload_to='media'),
        ),
    ]
