# Generated by Django 5.1.2 on 2024-10-13 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('label', models.CharField(max_length=255, unique=True)),
                ('balance', models.DecimalField(decimal_places=18, default=0, max_digits=36)),
            ],
        ),
    ]
