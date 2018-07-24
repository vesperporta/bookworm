"""Books app serializers."""

from rest_framework import serializers
from django.db import transaction

from authentication.serializers import AuthorSerializer, SmallAuthorSerializer
from bookworm.serializers import PreservedModelSerializeMixin, \
    ForeignFieldRepresentationSerializerMixin, ProfileSerializeMixin
from meta_info.serializers import MetaInfoAvailabledSerializerMixin
from posts.models import Post
from posts.serializers import EmotableAggregateSerializerMixin
from authentication.models import Profile

from file_store.models import (
    Image,
    Document,
)
from books.models import (
    Book,
    BookProgress,
    BookChapter,
    ReadingList,
    BookReview,
)
from books.models_read import (
    ConfirmReadQuestion,
    ConfirmReadAnswer,
    Read,
)


class BookReviewShortSerializer(
        EmotableAggregateSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """BookReview serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookreview-detail',
    )

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
        )
        exclude = []


class BookSerializer(
        EmotableAggregateSerializerMixin,
        ProfileSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
        PreservedModelSerializeMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Book model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='book-detail',
    )
    reviews = BookReviewShortSerializer(
        many=True,
        read_only=True,
    )
    documents = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='document-detail',
        queryset=Document.objects.all(),
        required=False,
        allow_null=True,
    )
    images = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )
    cover_image = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )
    author = AuthorSerializer(
        many=False,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Book
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'reviews',
            'meta_info',
            'emote_aggregate',
            'images',
            'profile',
        )
        fields = read_only_fields + (
            'title',
            'author',
            'description',
            'isbn',
            'ean',
            'documents',
            'cover_image',
        )
        exclude = []


class SmallBookSerializer(
        PreservedModelSerializeMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Book model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='book-detail',
    )
    cover_image = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )
    author = SmallAuthorSerializer(
        many=False,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Book
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'title',
            'author',
            'description',
            'cover_image',
        )
        fields = read_only_fields
        exclude = []


class BookProgressSerializer(
    ProfileSerializeMixin,
    serializers.HyperlinkedModelSerializer,
):
    """BookProgress model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookprogress-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    document = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='document-detail',
        queryset=Document.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BookProgress
        exclude = []
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'start',
            'end',
            'book',
            'document',
        )


class SmallBookProgressSerializer(serializers.HyperlinkedModelSerializer):
    """Small BookProgress model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookprogress-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )

    class Meta:
        model = BookProgress
        exclude = []
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'start',
            'end',
            'book',
        )


class BookChapterSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """BookChapter serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookchapter-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    progress = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='bookprogress-detail',
        queryset=BookProgress.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BookChapter
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'progress',
            'book',
        )
        exclude = []


class ReadingListSerializer(
        EmotableAggregateSerializerMixin,
        ProfileSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ReadingList serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='readinglist-detail',
    )
    books = SmallBookSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ReadingList
        read_only_fields = (
            'id',
            'profile',
            'created_at',
            'modified_at',
            'deleted_at',
            'books',
            'emote_aggregate',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'description',
        )
        exclude = []


class SmallReadingListSerializer(serializers.HyperlinkedModelSerializer):
    """Small ReadingList serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='readinglist-detail',
    )
    books = SmallBookSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ReadingList
        read_only_fields = (
            'id',
            'books',
            'title',
        )
        fields = read_only_fields
        exclude = []


class BookReviewSerializer(
    EmotableAggregateSerializerMixin,
    ProfileSerializeMixin,
    ForeignFieldRepresentationSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    """BookReview serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookreview-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    progress = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='progress-detail',
        queryset=BookProgress.objects.all(),
        required=False,
        allow_null=True,
    )
    post = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='post-detail',
        queryset=Post.objects.all(),
        required=False,
        allow_null=True,
    )
    copy = serializers.CharField()

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'emote_aggregate',
            'post',
        )
        fields = read_only_fields + (
            'type',
            'rating',
            'copy',
            'book',
            'progress',
        )
        exclude = ()
        foreign_fields_get = {
            'copy': 'post',
        }

    def create(self, validated_data):
        """Create a BookReview object with a Post object to store copy.

        @:param validated_data: dict validated from request data.

        @:returns BookReview
        """
        with transaction.atomic():
            created_post = Post.objects.create(
                copy=validated_data.get('copy'),
                profile=self.context['request'].user.profile,
            )
            validated_data.pop('copy')
            validated_data.update({
                'post': created_post,
            })
        return super().create(validated_data)


class ConfirmReadQuestionSerializer(
    ProfileSerializeMixin,
    EmotableAggregateSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    """ConfirmReadQuestion model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadquestion-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    chapter = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='bookchapter-detail',
        queryset=BookChapter.objects.all(),
        required=False,
        allow_null=True,
    )
    multi_choice_answer = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='confirmreadquestion-detail',
        queryset=ConfirmReadQuestion.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ConfirmReadQuestion
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'difficulty',
            'book',
            'chapter',
            'copy',
            'multi_choice_answer',
        )
        exclude = []


class ConfirmReadAnswerSerializer(
    ProfileSerializeMixin,
    serializers.HyperlinkedModelSerializer,
):
    """ConfirmReadAnswer model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadanswer-detail',
    )
    question = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='confirmreadquestion-detail',
        queryset=ConfirmReadQuestion.objects.all(),
    )

    class Meta:
        model = ConfirmReadAnswer
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'correct',
        )
        fields = read_only_fields + (
            'question',
            'is_true',
            'copy',
        )
        exclude = []


class ReadSerializer(
    ProfileSerializeMixin,
    EmotableAggregateSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    """ConfirmRead model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='read-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    answer = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='confirmreadanswer-detail',
        queryset=ConfirmReadAnswer.objects.all(),
    )
    post = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='post-detail',
        read_only=True,
    )

    class Meta:
        model = Read
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'answered_correctly',
            'emote_aggregate',
            'profile',
            'post',
        )
        fields = read_only_fields + (
            'book',
            'answer',
        )
        exclude = []

    def create(self, validated_data):
        answer_data = validated_data.pop('answer')
        if type(answer_data) is not str:
            validated_data.update(
                {'answer': ConfirmReadAnswerSerializer(data=answer_data).id, }
            )
        return super().create(validated_data)
