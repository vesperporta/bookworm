# Generated by Django 2.0.2 on 2018-04-25 12:52

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
            name='Comment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('copy', models.CharField(max_length=400, verbose_name='Comment copy')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts+', to='meta_info.MetaInfo', verbose_name='Meta data')),
            ],
            options={
                'verbose_name': "Posts' Comment",
                'verbose_name_plural': "Posts' Comments",
            },
        ),
        migrations.CreateModel(
            name='Emote',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(0, '👓'), (1, '❤️'), (2, '😂'), (3, '💀'), (4, '💩'), (5, '😕'), (6, '\U0001f92c')])),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='emotes', to='posts.Comment', verbose_name='Comment')),
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
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('copy', models.TextField(verbose_name='Post copy')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('published_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_content+', to='meta_info.MetaInfo', verbose_name='Published Content')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.AddField(
            model_name='emote',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='emotes', to='posts.Post', verbose_name='Posting'),
        ),
        migrations.AddField(
            model_name='emote',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='posts.Post', verbose_name='Posting'),
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='published_content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_content+', to='meta_info.MetaInfo', verbose_name='Published Content'),
        ),
        migrations.AlterUniqueTogether(
            name='emote',
            unique_together={('profile', 'post'), ('profile', 'comment')},
        ),
    ]
