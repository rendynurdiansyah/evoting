# Generated by Django 5.0.6 on 2024-06-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_remove_voting_encrypted_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voting',
            old_name='timestamp',
            new_name='waktu_voting',
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='voting',
            name='judul_pemilihan',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='voting',
            name='nama_kandidat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='voting',
            name='nama_pemilih',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='voting',
            name='kandidat',
        ),
        migrations.RemoveField(
            model_name='voting',
            name='pemilih',
        ),
        migrations.RemoveField(
            model_name='voting',
            name='pemilihan',
        ),
    ]