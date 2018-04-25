# Generated by Django 2.0.2 on 2018-04-24 20:48

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
            name='Book',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('isbn', models.CharField(blank=True, db_index=True, max_length=16, verbose_name='International Standard Book Number')),
                ('ean', models.CharField(blank=True, db_index=True, max_length=16, verbose_name='International Article Number')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('localisations', models.ManyToManyField(blank=True, related_name='_book_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localised Copy')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='books+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('published_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_content+', to='meta_info.MetaInfo', verbose_name='Published Content')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='BookChapter',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='chapters', to='books.Book', verbose_name='Book')),
                ('localisations', models.ManyToManyField(blank=True, related_name='_bookchapter_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localised Copy')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_chapters+', to='meta_info.MetaInfo', verbose_name='Meta data')),
            ],
            options={
                'verbose_name': "Books' chapter",
                'verbose_name_plural': "Books' chapters",
            },
        ),
        migrations.CreateModel(
            name='BookProgress',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('percent', models.FloatField()),
                ('page', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start', models.BigIntegerField()),
                ('end', models.BigIntegerField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='progress+', to='books.Book', verbose_name='Book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Progress',
                'verbose_name_plural': 'Progresses',
            },
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(blank=True, choices=[(0, 'Review'), (1, 'Footnote'), (2, 'Margin note'), (3, 'Line highlight'), (4, 'Paragraph highlight')], default=0)),
                ('copy', models.TextField(db_index=True)),
                ('rating', models.IntegerField(blank=True, choices=[(0, 'Unrated'), (1, 'Terrible and Trashy'), (2, 'Junk Pile'), (3, 'Readable'), (4, 'Good Read'), (5, "Couldn't Put Down")], default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews', to='books.Book', verbose_name='Book')),
                ('localisations', models.ManyToManyField(blank=True, related_name='_bookreview_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localised Copy')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_reviews+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('progress', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewed_at', to='books.BookProgress', verbose_name='Progress')),
                ('published_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_content+', to='meta_info.MetaInfo', verbose_name='Published Content')),
            ],
            options={
                'verbose_name': "Reader' book review",
                'verbose_name_plural': "Readers' book reviews",
            },
        ),
        migrations.CreateModel(
            name='ConfirmReadAnswer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('answer', models.BooleanField(default=False, verbose_name='Is Answer')),
                ('copy', models.CharField(max_length=240, verbose_name='Answer Copy')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Confirm Read Answer',
                'verbose_name_plural': 'Confirm Read Answers',
            },
        ),
        migrations.CreateModel(
            name='ConfirmReadQuestion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('difficulty', models.IntegerField(blank=True, choices=[(0, 'Basic: Read the title.'), (1, 'Simple: Highlight question.'), (2, 'Normal: Read the book.'), (3, 'Hard: Full on factual.'), (4, 'Transcend: 🖖')], default=1)),
                ('question', models.CharField(max_length=240, verbose_name='Question')),
                ('book', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='confirm_read+', to='books.Book', verbose_name='Book')),
                ('chapter', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='confirm_read+', to='books.BookChapter', verbose_name='Chapter')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Confirm Read Question',
                'verbose_name_plural': 'Confirm Read Questions',
            },
        ),
        migrations.CreateModel(
            name='Read',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='read_selected', to='books.ConfirmReadAnswer', verbose_name='Challenge Answer')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='read', to='books.Book', verbose_name='Book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='read', to='books.ConfirmReadQuestion', verbose_name='Question Challenge')),
            ],
            options={
                'verbose_name': 'Read',
                'verbose_name_plural': 'Read',
            },
        ),
        migrations.CreateModel(
            name='ReadingList',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('books', models.ManyToManyField(related_name='reading_lists', to='books.Book', verbose_name='Books')),
                ('localisations', models.ManyToManyField(blank=True, related_name='_readinglist_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localised Copy')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reading_lists+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('published_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_content+', to='meta_info.MetaInfo', verbose_name='Published Content')),
            ],
            options={
                'verbose_name': 'Reading List',
                'verbose_name_plural': 'Reading Lists',
            },
        ),
        migrations.CreateModel(
            name='Thrill',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='thrills', to='books.Book', verbose_name='Book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('reading_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='thrills', to='books.ReadingList', verbose_name='Reading List')),
            ],
            options={
                'verbose_name': 'Thrill',
                'verbose_name_plural': 'Thrills',
            },
        ),
        migrations.AddField(
            model_name='confirmreadanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='books.ConfirmReadQuestion', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='bookchapter',
            name='progress',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='chapter_progress+', to='books.BookProgress', verbose_name='Progress'),
        ),
    ]
