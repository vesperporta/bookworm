from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'books'
    verbose_name = 'Publications and Books'

    def ready(self):
        from books import models_read  # noqa
        from books import signals  # noqa
