from rest_framework import serializers
from .models import PostComments


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='user.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = PostComments
        fields = ['comment_id', 'post', 'comment', 'parent', 'timestamp', 'author_name', 'author_avatar']

    def get_author_avatar(self, obj):
        return getattr(obj.user.profile, 'avatar', None) if hasattr(obj.user, 'profile') else None
