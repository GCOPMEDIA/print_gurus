from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('all-posts/', all_posts,name='all_posts'),
    path('about/',about,name='about'),
path('like-post/<int:post_id>/', like_post),
    path("csrf/",get_csrf),
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]