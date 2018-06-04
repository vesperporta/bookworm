# Generated by Django 2.0.2 on 2018-06-04 13:46

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('meta_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emote',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(0, '👓'), (1, '❤️'), (2, '😂'), (3, '💀'), (4, '💩'), (5, '😕'), (6, '\U0001f92c')])),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Emote',
                'verbose_name_plural': 'Emotes',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Published date')),
                ('emote_aggregate', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, null=True, size=8, verbose_name='Emote Aggregate')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('copy', models.TextField(verbose_name='Post copy')),
                ('emotes', models.ManyToManyField(blank=True, related_name='_post_emotes_+', to='posts.Emote', verbose_name='Emotes')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='posts.Post', verbose_name='Parent Post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('published_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_content+', to='meta_info.MetaInfo', verbose_name='Published Content')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
