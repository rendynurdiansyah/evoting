# Generated by Django 5.0.6 on 2024-06-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_voting_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='encrypted_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
