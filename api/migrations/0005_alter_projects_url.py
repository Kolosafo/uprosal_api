# Generated by Django 4.1.7 on 2023-04-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_letter_coverletter_cover_letter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]