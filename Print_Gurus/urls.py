from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
# router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('all-posts/', all_posts,name='all_posts'),
    path('about/',about,name='about'),
path('like-post/<int:post_id>/', like_post),
    path("csrf/",get_csrf),
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup',signup_view),
    path('', include(router.urls)),
    path('check/',check_auth,name='check'),
    path('comment/',comment),
    path('all-comments/',get_all_comments),
    path('reply/',reply),
    path('events/',events)
]