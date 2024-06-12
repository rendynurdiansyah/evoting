# Generated by Django 5.0.6 on 2024-06-10 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_pemilih'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kandidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('visi_misi', models.TextField()),
                ('foto', models.ImageField(upload_to='foto/')),
            ],
        ),
    ]