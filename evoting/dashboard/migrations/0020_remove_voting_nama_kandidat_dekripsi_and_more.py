# Generated by Django 5.0.6 on 2024-06-23 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_alter_pemilihan_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting',
            name='nama_kandidat_dekripsi',
        ),
        migrations.AlterField(
            model_name='voting',
            name='judul_pemilihan',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='voting',
            name='nama_kandidat',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='voting',
            name='nama_pemilih',
            field=models.TextField(blank=True, null=True),
        ),
    ]
