# Generated by Django 5.0.6 on 2024-06-09 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_voting_pemilihan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pemilih',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nim', models.CharField(max_length=20)),
                ('prodi', models.CharField(max_length=100)),
                ('org_hima', models.CharField(max_length=100)),
                ('org_ukm', models.CharField(max_length=100)),
            ],
        ),
    ]
