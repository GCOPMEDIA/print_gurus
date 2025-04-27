import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
# Create your views here.
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView


def all_posts(request):
    data_blogs = []
    blogs = BlogPost.objects.all()
    for i in blogs:
        data_blogs.append({
            'id': i.blog_id,
            'title': i.blog_title,
            'subtitle': i.blog_subtitle,
            'body': i.blog_body,
            'media': f"{i.blog_media.url}" if i.blog_media else "",
            'video_url': i.video_url,
            'created_by': i.created_by.first_name,
            "like_count": i.like_count,
            'url': f"/article/{i.blog_id}"
        })

    return JsonResponse(data_blogs, safe=False)


# class BlogList(APIView):
#     def get(self,request):
#         post = BlogPost.objects.all()
#         data_blogs = {'title': i.blog_title for i in post}
#         return Response(data_blogs)
from django.http import JsonResponse
from .models import Leaders

from django.http import JsonResponse
from .models import Leaders

from django.http import JsonResponse
from .models import Leaders


def about(request):
    # Retrieve all leaders and related image field (optimizing with select_related if needed)
    leaders = Leaders.objects.all()

    # Prepare leader data
    first_leader = None
    clergy = []
    elders = []
    deacons = []
    workers = []

    for leader in leaders:
        leader_data = {
            "leader_title": leader.leader_title,
            "leader_name": leader.leader_name,
            "leader_image": f"{leader.leader_image.url}" if leader.leader_image else '',  # Accessing image URL
            "leader_branch": leader.leader_branch or '',  # Default to empty string if no branch
        }

        # Categorize leaders
        if leader.leader_title == "Founder":
            first_leader = leader_data
        elif leader.leader_title == "Pastor":
            clergy.append(leader_data)
        elif leader.leader_title == "Elder":
            elders.append(leader_data)
        elif leader.leader_title == "Deacon":
            deacons.append(leader_data)
        elif leader.leader_title == "Worker":
            workers.append(leader_data)

    # Return JSON response
    data = {
        "first_leader": first_leader,
        "clergy": clergy,
        "elder": elders,
        "deacons": deacons,
        "workers": workers,
    }

    return JsonResponse(data, safe=False)


def login(request):
    pass


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        try:
            post = BlogPost.objects.get(blog_id=post_id)
            post.like_count += 1
            post.save()
            return JsonResponse({'likes': post.like_count})
        except BlogPost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)


from django.middleware.csrf import get_token


def get_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.timezone import now

from rest_framework.decorators import api_view
from rest_framework import status
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import IntegrityError


@api_view(['POST'])
def signup_view(request):
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            first_name=data.get('f_name', ''),
            last_name=data.get('l_name', ''),
            username=username,
            email=email,
            password=password,
            is_staff=False,
            date_joined=now()
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        if "UNIQUE constraint failed: auth_user.username" in str(e):
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        elif "UNIQUE constraint failed: auth_user.email" in str(e):
            return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from .models import PostComments
# from .serializers import CommentSerializer

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = PostComments.objects.select_related('user', 'post', 'parent').all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_queryset(self):
#         post_id = self.request.query_params.get('post_id')
#         if post_id:
#             return self.queryset.filter(post_id=post_id)
#         return self.queryset.none()  # Don't return all comments unless filtering
#
#     @action(detail=False, methods=['get'])
#     def for_post(self, request):
#         post_id = request.query_params.get('post_id')
#         comments = self.get_queryset().filter(post_id=post_id, parent=None).order_by('-timestamp')
#         serializer = self.get_serializer(comments, many=True)
#         return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def check_auth(request):
    return Response({"user": str(request.user), "auth": str(request.auth)})


@api_view(['POST'])
def comment(request):
    data = request.data
    username = data.get('username')
    post_id = data.get('post_id')
    comment_body = data.get('comment')

    if not username or not post_id or not comment_body:
        return Response({'error': 'Oops Bad Request, missing fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post_obj = BlogPost.objects.get(blog_id=post_id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Oops Post Not Found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user = AuthUser.objects.get(username=username)
    except AuthUser.DoesNotExist:
        return Response({'error': 'Oops User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    # Save the comment
    c = Comments(
        post=post_obj,
        user=user,
        comment=comment_body
    )
    c.save()

    return Response({'message': 'Comment added successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_all_comments(request):
    post_id = request.query_params.get('post_id')

    if not post_id:
        return Response({'error': 'Oops No Post To Comment on'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post_obj = BlogPost.objects.get(blog_id=post_id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Oops Post Not Found'}, status=status.HTTP_404_NOT_FOUND)

    # Fetch all comments related to the post
    comments = Comments.objects.filter(post=post_obj)  # only top-level comments

    all_comments = []
    for comment in comments:
        # Fetch replies to each comment
        replies = Reply.objects.filter(comment=comment)

        reply_list = [
            {
                'id': reply.reply_id,
                'username': reply.user.username,
                'comment': reply.reply
            }
            for reply in replies
        ]

        all_comments.append({
            'id': comment.comment_id,
            'username': comment.user.username,
            'comment': comment.comment,
            'replies': reply_list  # attach replies here
        })

    return Response({'comments': all_comments})


@api_view(['POST'])
def reply(request):
    data = request.data
    comment_id = data.get('parent')
    reply_text = data.get('text')
    user = data.get('username')
    if not comment_id or not reply_text or not user:
        return Response({'error': 'Oops Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        c = Comments.objects.get(comment_id=comment_id)

    except Comments.DoesNotExist:
        return Response({'error': 'Oops  Comment Not Found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        u = AuthUser.objects.get(username=user)

    except AuthUser.DoesNotExist:
        return Response({'error': 'Oops User Not Found'}, status=status.HTTP_404_NOT_FOUND)
    r = Reply(comment=c,
              user=u,
              reply=reply_text)
    r.save()
    return Response({'message': 'Reply added successfully!'}, status=status.HTTP_201_CREATED)


