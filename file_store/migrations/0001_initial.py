# Generated by Django 2.0.2 on 2018-05-24 09:28

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('books', '0001_initial'),
        ('meta_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayImage',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('extension', models.CharField(blank=True, max_length=20)),
                ('mime', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(upload_to='')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='books.Book', verbose_name='Book')),
                ('circle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='authentication.Circle', verbose_name="Circles' image")),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='files+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('original', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sizes', to='file_store.DisplayImage', verbose_name='Cropped Images')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('progress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_progress+', to='books.BookProgress', verbose_name='Progress')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='StoredFile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('extension', models.CharField(blank=True, max_length=20)),
                ('mime', models.CharField(blank=True, max_length=50)),
                ('file', models.FileField(null=True, upload_to='')),
                ('url', models.URLField(blank=True, max_length=2000, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='files', to='books.Book', verbose_name='Book')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='files+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('progress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_progress+', to='books.BookProgress', verbose_name='Progress')),
            ],
            options={
                'verbose_name': 'Publication File',
                'verbose_name_plural': "Publications' Files",
            },
        ),
    ]
