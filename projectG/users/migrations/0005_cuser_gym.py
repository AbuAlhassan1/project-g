# Generated by Django 4.2.3 on 2023-08-19 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
        ('users', '0004_cuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuser',
            name='gym',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='gym.gym'),
        ),
    ]
