# Generated by Django 3.2.7 on 2023-03-30 15:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_user_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQouta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('Not Activated', 'Not Activated'), ('Trial', 'Trial'), ('Trial Ended', 'Trial Ended'), ('Subscription Expired', 'Subscription Expired'), ('Pro', 'Pro'), ('Business', 'Business'), ('Enterprise', 'Enterprise')], default='Trial', max_length=20)),
                ('qouta', models.FloatField()),
                ('date_updated', models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 30, 15, 3, 4, 455685, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 30, 15, 3, 4, 455685, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Not Activated', 'Not Activated'), ('Trial', 'Trial'), ('Trial Ended', 'Trial Ended'), ('Subscription Expired', 'Subscription Expired'), ('Pro', 'Pro'), ('Business', 'Business'), ('Enterprise', 'Enterprise')], default='Not Activated', max_length=20),
        ),
    ]
