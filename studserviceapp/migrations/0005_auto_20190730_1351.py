# Generated by Django 2.2.3 on 2019-07-30 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studserviceapp', '0004_auto_20190723_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terminpolaganja',
            name='nastavnik',
        ),
        migrations.AddField(
            model_name='terminpolaganja',
            name='nastavnik',
            field=models.ManyToManyField(to='studserviceapp.Nastavnik'),
        ),
    ]
