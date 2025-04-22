from django.shortcuts import render
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
            'media': f"{i.blog_media.url}",
            'video_url': i.video_url,
            'created_by': i.created_by.first_name,
            "like_count": i.like_count,
            'url': f"/article/{i.blog_id}"
        })
    print(data_blogs)
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
        if leader.leader_title == "General Overseer":
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

