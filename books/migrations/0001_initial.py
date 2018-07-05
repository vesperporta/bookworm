# Generated by Django 2.0.2 on 2018-07-05 16:43

import books.policies
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('authentication', '0001_initial'),
        ('meta_info', '0001_initial'),
        ('file_store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('emote_aggregate', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, null=True, size=8, verbose_name='Emote Aggregate')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('isbn', models.CharField(blank=True, max_length=10, verbose_name='International Standard Book Number')),
                ('ean', models.CharField(blank=True, db_index=True, max_length=13, verbose_name='International Article Number')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='books', to='authentication.Author', verbose_name='Author')),
                ('cover_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='album_covers+', to='file_store.Image', verbose_name='Cover Image')),
                ('documents', models.ManyToManyField(blank=True, related_name='shelves', to='file_store.Document', verbose_name='Documents')),
                ('emotes', models.ManyToManyField(blank=True, related_name='_book_emotes_+', to='posts.Emote', verbose_name='Emotes')),
                ('images', models.ManyToManyField(blank=True, related_name='_book_images_+', to='file_store.Image', verbose_name='Images')),
                ('localisations', models.ManyToManyField(blank=True, related_name='_book_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localisation')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='books+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
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
                ('localisations', models.ManyToManyField(blank=True, related_name='_bookchapter_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localisation')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_chapters+', to='meta_info.MetaInfo', verbose_name='Meta data')),
            ],
            options={
                'verbose_name': 'Book Chapter',
                'verbose_name_plural': 'Book Chapters',
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
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='coffee_table+', to='file_store.Document', verbose_name='Document')),
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
                ('emote_aggregate', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, null=True, size=8, verbose_name='Emote Aggregate')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('type', models.IntegerField(blank=True, choices=[(0, 'Review'), (1, 'Footnote'), (2, 'Margin note'), (3, 'Line highlight'), (4, 'Paragraph highlight')], default=0)),
                ('copy', models.TextField(db_index=True)),
                ('rating', models.IntegerField(blank=True, choices=[(0, 'Unrated'), (1, 'Terrible and Trashy'), (2, 'Junk Pile'), (3, 'Readable'), (4, 'Good Read'), (5, "Couldn't Put Down")], default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews', to='books.Book', verbose_name='Book')),
                ('emotes', models.ManyToManyField(blank=True, related_name='_bookreview_emotes_+', to='posts.Emote', verbose_name='Emotes')),
                ('inferred_progress', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inferred_reviewed_at+', to='books.BookProgress', verbose_name='Inferred Progress')),
                ('localisations', models.ManyToManyField(blank=True, related_name='_bookreview_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localisation')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_reviews+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
                ('progress', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewed_at', to='books.BookProgress', verbose_name='Progress')),
                ('published_meta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_meta+', to='meta_info.MetaInfo', verbose_name='Published Content')),
            ],
            options={
                'verbose_name': 'Book Review',
                'verbose_name_plural': 'Book Reviews',
            },
        ),
        migrations.CreateModel(
            name='ConfirmReadAnswer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('copy', models.CharField(max_length=400, verbose_name='Answer copy')),
                ('lock', models.BooleanField(default=False, verbose_name='Lock Changes')),
                ('is_true', models.BooleanField(default=None, verbose_name='Boolean Answer')),
                ('is_answer', models.BooleanField(default=False, verbose_name='Is Answer for Multiple Choice')),
                ('accepted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Accepted When')),
                ('accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='read_answers_accepted+', to='authentication.Profile', verbose_name='Accepted By')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Confirm Read Answer',
                'verbose_name_plural': 'Confirm Read Answers',
            },
            bases=(models.Model, books.policies.OwnerElevatedAndLockAccessMixin),
        ),
        migrations.CreateModel(
            name='ConfirmReadQuestion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('emote_aggregate', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, null=True, size=8, verbose_name='Emote Aggregate')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('difficulty', models.IntegerField(blank=True, choices=[(0, 'Basic: Read the title.'), (1, 'Simple: Highlight question.'), (2, 'Normal: Read the book.'), (3, 'Hard: Full on factual.'), (4, 'Transcend: 🖖')], default=1)),
                ('copy', models.CharField(max_length=400, verbose_name='Question')),
                ('lock', models.BooleanField(default=False, verbose_name='Lock Changes')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='confirm_read+', to='books.Book', verbose_name='Book')),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='confirm_read+', to='books.BookChapter', verbose_name='Chapter')),
                ('emotes', models.ManyToManyField(blank=True, related_name='_confirmreadquestion_emotes_+', to='posts.Emote', verbose_name='Emotes')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Confirm Read Question',
                'verbose_name_plural': 'Confirm Read Questions',
            },
            bases=(models.Model, books.policies.OwnerElevatedAndLockAccessMixin),
        ),
        migrations.CreateModel(
            name='Read',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('emote_aggregate', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, null=True, size=8, verbose_name='Emote Aggregate')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('answer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='read_selected', to='books.ConfirmReadAnswer', verbose_name='Challenge Answer')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='read', to='books.Book', verbose_name='Book')),
                ('emotes', models.ManyToManyField(blank=True, related_name='_read_emotes_+', to='posts.Emote', verbose_name='Emotes')),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='read+', to='posts.Post', verbose_name='Comment Thread')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
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
                ('emote_aggregate', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), blank=True, null=True, size=8, verbose_name='Emote Aggregate')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('books', models.ManyToManyField(related_name='reading_lists', to='books.Book', verbose_name='Books')),
                ('emotes', models.ManyToManyField(blank=True, related_name='_readinglist_emotes_+', to='posts.Emote', verbose_name='Emotes')),
                ('localisations', models.ManyToManyField(blank=True, related_name='_readinglist_localisations_+', to='meta_info.LocaliseTag', verbose_name='Localisation')),
                ('meta_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reading_lists+', to='meta_info.MetaInfo', verbose_name='Meta data')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.Profile')),
            ],
            options={
                'verbose_name': 'Reading List',
                'verbose_name_plural': 'Reading Lists',
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
