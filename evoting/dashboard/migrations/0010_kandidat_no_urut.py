# Generated by Django 5.0.6 on 2024-06-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_pemilihan_is_election_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='kandidat',
            name='no_urut',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
