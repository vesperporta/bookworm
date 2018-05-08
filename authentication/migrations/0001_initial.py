# Generated by Django 2.0.2 on 2018-05-08 08:50

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name_title', models.IntegerField(blank=True, choices=[(0, 'Mrs'), (1, 'Mr'), (2, 'Miss'), (3, 'Ms'), (4, 'Dr'), (5, 'Sir')], null=True)),
                ('name_first', models.CharField(db_index=True, max_length=64)),
                ('name_family', models.CharField(db_index=True, max_length=64)),
                ('name_middle', models.CharField(blank=True, max_length=128, null=True)),
                ('name_display', models.CharField(blank=True, max_length=254)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('death_date', models.DateField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=254, verbose_name='Reading Circle Title')),
            ],
            options={
                'verbose_name': 'Circle',
                'verbose_name_plural': 'Circles',
            },
        ),
        migrations.CreateModel(
            name='CircleSetting',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('copy', models.TextField(blank=True, db_index=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='settings', to='authentication.Circle', verbose_name='Settings for Circle')),
                ('tags', models.ManyToManyField(blank=True, related_name='_circlesetting_tags_+', to='meta_info.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Circle Setting',
                'verbose_name_plural': 'Circle Settings',
            },
        ),
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(blank=True, choices=[(0, 'Email'), (1, 'Mobile Number'), (2, 'Landline Number'), (3, 'Postal Address'), (4, 'Billing Address'), (5, 'Social Network ID')], default=0)),
                ('detail', models.TextField(db_index=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True)),
                ('uri', models.URLField(blank=True, null=True)),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contacts+', to='meta_info.MetaInfo', verbose_name='Meta data')),
            ],
            options={
                'verbose_name': 'Contact Method',
                'verbose_name_plural': 'Contact Methods',
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Invited'), (1, 'Accepted'), (2, 'Rejected'), (3, 'Withdrawn'), (4, 'Banned'), (5, 'Elevated')], default=0)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='invitations', to='authentication.Circle', verbose_name='Circle invited to')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='invitation_meta+', to='meta_info.MetaInfo', verbose_name='Invitation meta data')),
            ],
            options={
                'verbose_name': 'Invitation',
                'verbose_name_plural': 'Invitations',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name_title', models.IntegerField(blank=True, choices=[(0, 'Mrs'), (1, 'Mr'), (2, 'Miss'), (3, 'Ms'), (4, 'Dr'), (5, 'Sir')], null=True)),
                ('name_first', models.CharField(db_index=True, max_length=64)),
                ('name_family', models.CharField(db_index=True, max_length=64)),
                ('name_middle', models.CharField(blank=True, max_length=128, null=True)),
                ('name_display', models.CharField(blank=True, max_length=254)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('death_date', models.DateField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(blank=True, choices=[(0, 'User'), (1, 'Elevated'), (2, 'Administrator'), (3, 'Destroyer of Worlds')], default=0)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('contacts', models.ManyToManyField(related_name='_profile_contacts_+', to='authentication.ContactMethod', verbose_name='Contact Methods')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profiles+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name="Profiles' User")),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='ProfileSetting',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('copy', models.TextField(blank=True, db_index=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='settings', to='authentication.Profile', verbose_name='Profile')),
                ('tags', models.ManyToManyField(blank=True, related_name='_profilesetting_tags_+', to='meta_info.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Profile Setting',
                'verbose_name_plural': 'Profile Settings',
            },
        ),
        migrations.AddField(
            model_name='invitation',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='profile_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='invitations', to='authentication.Profile', verbose_name='Profile Invited'),
        ),
        migrations.AddField(
            model_name='circle',
            name='contacts',
            field=models.ManyToManyField(related_name='_circle_contacts_+', to='authentication.ContactMethod', verbose_name='Contact Methods'),
        ),
        migrations.AddField(
            model_name='circle',
            name='meta_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='circles_meta+', to='meta_info.MetaInfo', verbose_name='Circles meta data'),
        ),
        migrations.AddField(
            model_name='circle',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='circles', to='authentication.Profile', verbose_name='Created by'),
        ),
    ]
