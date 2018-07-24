"""Tasks to delay from web serve thread."""

def answer_accepted_create_read_task(accepted_answer):
    """Task to handle the decoupled creation of a Read object.

    @:param accepted_answer: ConfirmReadAnswer accepted by elevated Profile.

    @:returns Read
    """
    from books.models_read import Read
    from posts.models import Post
    post = Post.objects.create(
        copy=f'{Read.PREFIX}: Read this awesome book, ⭐️!',
        profile=accepted_answer.profile,
    )
    return Read.objects.create(
        book=accepted_answer.question.book,
        answer=accepted_answer,
        post=post,
        profile=accepted_answer.profile,
    )
