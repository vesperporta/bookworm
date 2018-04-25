from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Posts on profiles and Reading Circles'

    def ready(self):
        from posts import signals  # noqa
