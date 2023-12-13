# Generated by Django 3.2.20 on 2023-12-13 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('is_regenerate', models.BooleanField(default=False)),
            ],
        ),
    ]
