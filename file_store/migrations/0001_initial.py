# Generated by Django 2.0.2 on 2018-07-24 11:10

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meta_info', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('title', models.CharField(blank=True, db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('extension', models.CharField(blank=True, max_length=50, null=True)),
                ('mime', models.CharField(blank=True, max_length=50, null=True)),
                ('source_url', models.URLField(blank=True, max_length=2000, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('file', models.FileField(null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('title', models.CharField(blank=True, db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('extension', models.CharField(blank=True, max_length=50, null=True)),
                ('mime', models.CharField(blank=True, max_length=50, null=True)),
                ('source_url', models.URLField(blank=True, max_length=2000, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='images+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('original', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sizes', to='file_store.Image', verbose_name='Cropped Images')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='covers+', to='file_store.Image', verbose_name='Cover Image'),
        ),
        migrations.AddField(
            model_name='document',
            name='meta_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='files+', to='meta_info.MetaInfo', verbose_name='Meta data'),
        ),
        migrations.AddField(
            model_name='document',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile'),
        ),
    ]
