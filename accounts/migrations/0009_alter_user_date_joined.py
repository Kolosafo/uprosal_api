# Generated by Django 4.1.7 on 2023-03-29 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 29, 10, 29, 16, 295541, tzinfo=datetime.timezone.utc)),
        ),
    ]
