"""Books app serializers."""

from rest_framework import serializers

from authentication.serializers import AuthorSerializer
from bookworm.serializers import PreservedModelSerializeMixin
from meta_info.serializers import MetaInfoAvailabledSerializerMixin
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
        PreservedModelSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
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
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
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


class BookProgressSerializer(
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
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
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
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ReadingList serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='readinglist-detail',
    )
    books = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
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
        )
        exclude = []


class BookReviewSerializer(
        EmotableAggregateSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
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
        view_name='bookprogress-detail',
        queryset=BookProgress.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'profile',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
            'book',
            'progress',
        )
        exclude = []


class ConfirmReadQuestionSerializer(
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
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
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
        )
        exclude = []


class ConfirmReadAnswerSerializer(
        serializers.HyperlinkedModelSerializer,
):
    """ConfirmReadAnswer model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadanswer-detail',
    )
    accepted_by = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )
    question = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='confirmreadquestion-detail',
        queryset=ConfirmReadQuestion.objects.all(),
    )
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )

    class Meta:
        model = ConfirmReadAnswer
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'accepted_at',
            'accepted_by',
        )
        fields = read_only_fields + (
            'question',
            'is_true',
            'is_answer',
            'copy',
        )
        exclude = []


class ReadSerializer(
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
    answered_correctly = serializers.BooleanField(
        read_only=True,
    )
    answer = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='confirmreadanswer-detail',
        queryset=ConfirmReadAnswer.objects.all(),
    )
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
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
