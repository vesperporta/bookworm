# Generated by Django 2.0.2 on 2018-03-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_readinglist_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='readinglist',
            old_name='date_read',
            new_name='finished_date',
        ),
        migrations.RenameField(
            model_name='readinglist',
            old_name='read',
            new_name='finished_reading',
        ),
        migrations.AddField(
            model_name='readinglist',
            name='started_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='readinglist',
            name='started_reading',
            field=models.BooleanField(default=False),
        ),
    ]
