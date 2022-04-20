from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404

from .mixins import MultiMixin
from reviews.models import Category, Genre, Review, Title
from .pagination import CommonPagination
from .permissions import IsAdminOrReadOnly, IsOwner
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, GetTitleSerializer,
                          NewTitleSerializer, ReviewsSerializer)
from .title_filter import TitleFilter


class CommentsViewSet(viewsets.ModelViewSet):

    serializer_class = CommentsSerializer
    permission_classes = (IsOwner,)
    pagination_class = CommonPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsOwner,)

    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class GenresViewSet(MultiMixin):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)


class CategoriesViewSet(MultiMixin):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = GetTitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTitleSerializer
        return NewTitleSerializer
