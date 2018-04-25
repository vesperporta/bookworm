# Generated by Django 2.0.2 on 2018-04-24 20:48

from django.conf import settings
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
            name='Circle',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=254, verbose_name='Reading Circle Title')),
                ('meta_info', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='circles_meta+', to='meta_info.MetaInfo', verbose_name='Circles meta data')),
            ],
            options={
                'verbose_name': 'Circle',
                'verbose_name_plural': 'Circles',
            },
        ),
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(blank=True, choices=[(0, 'email'), (1, 'mobile number'), (2, 'landline number'), (3, 'postal address'), (4, 'billing address'), (5, 'social network id')], default=0)),
                ('detail', models.TextField(db_index=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True)),
                ('uri', models.URLField(blank=True, null=True)),
                ('circle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contacts', to='authentication.Circle', verbose_name='Circle')),
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
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('name_title', models.IntegerField(blank=True, choices=[(0, 'Mrs'), (1, 'Mr'), (2, 'Miss'), (3, 'Ms'), (4, 'Dr'), (5, 'Sir')], null=True)),
                ('name_first', models.CharField(db_index=True, max_length=64)),
                ('name_family', models.CharField(db_index=True, max_length=64)),
                ('name_middle', models.CharField(blank=True, max_length=128, null=True)),
                ('name_display', models.CharField(blank=True, max_length=254)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profiles+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name="Profiles' User")),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
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
            model_name='contactmethod',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contacts', to='authentication.Profile', verbose_name='Profile'),
        ),
        migrations.AddField(
            model_name='circle',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='circles', to='authentication.Profile', verbose_name='Created by'),
        ),
    ]
