# Generated by Django 5.0.6 on 2024-06-23 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_voting_nama_kandidat_dekripsi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemilihan',
            name='token',
            field=models.CharField(editable=False, max_length=32, unique=True),
        ),
    ]