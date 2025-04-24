# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from ckeditor.fields import RichTextField

from cloudinary.models import CloudinaryField
import uuid



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
class BlogPost(models.Model):
    blog_id = models.AutoField(primary_key=True,)
    blog_title = models.CharField(null=False,blank=False,max_length=250)
    blog_subtitle = models.CharField(null=True,blank=True,max_length=450)
    blog_body = RichTextField()
    blog_media = CloudinaryField('image',blank=True,null=True)
    video_url = models.CharField(blank=True,null=True,max_length=1500)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    like_count = models.IntegerField(default=0)



    class Meta:
        managed = True
        db_table = 'blog_post'

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(null=False,blank=False,max_length=250)
    event_subtitle = models.CharField(null=True,blank=True,max_length=300)
    event_venue = models.CharField(null=True,blank=True,max_length=250)
    event_time = models.CharField(null=True,blank=True,max_length=250)
    event_body = models.CharField(null=True,blank=True,max_length=1500)
    event_date = models.CharField(null=True,blank=True,max_length=250)
    event_image = CloudinaryField('image',blank=True,null=True)
    event_video = CloudinaryField(resource_type='video',blank=True,null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    class Mate:
        managed = True
        db_table = 'events'

class Leaders(models.Model):
    leader_id = models.AutoField(primary_key=True)
    leader_name = models.CharField(null=False,blank=False,max_length=400)
    leader_title = models.CharField(null=False,blank=False,max_length=400)
    leader_image = CloudinaryField('image',blank=False,null=False)
    leader_branch = models.CharField(null=True,blank=True,max_length=250)

    class Meta:
        managed = True
        db_table = 'leaders'


class Like(models.Model):
    anonymous_user_id = models.CharField(max_length=36)  # Stores UUID as a string
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("anonymous_user_id", "post")  # Prevent duplicate likes


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'created_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(created_by_id=request.user)

    def save_model(self, request, obj, form, change):

        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(BlogPost, BlogPostAdmin)

class EventsAdmin(admin.ModelAdmin):
    list_display = ('event_title','created_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by_id=request.user)
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Events,EventsAdmin)

class AboutPageBackground(models.Model):
    image_id = models.AutoField(primary_key=True)
    background_image = CloudinaryField('image',blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'aboutBackground'


