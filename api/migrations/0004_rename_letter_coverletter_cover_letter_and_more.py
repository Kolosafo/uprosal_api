# Generated by Django 4.1.7 on 2023-04-02 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_coverletter_user_alter_projects_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coverletter',
            old_name='letter',
            new_name='cover_letter',
        ),
        migrations.AddField(
            model_name='coverletter',
            name='job_description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
