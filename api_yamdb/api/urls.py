from django.urls import include, path
from rest_framework import routers

from users.views import TokenObtainView, UserSignUpView, UserViewSet
from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, TitlesViewSet)

router = routers.DefaultRouter()
router.register('titles', TitlesViewSet, 'Title')
router.register('categories', CategoriesViewSet, 'Category')
router.register('genres', GenresViewSet, 'Genre')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]
