from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('all-posts/', all_posts,name='all_posts'),
    path('about/',about,name='about'),
path('like-post/<int:post_id>/', like_post),
    path("csrf/",get_csrf)

]