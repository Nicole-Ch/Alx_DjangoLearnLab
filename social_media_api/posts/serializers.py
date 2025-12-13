from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def validate_title(self,data):
        if len(data) < 5:
            raise serializers.ValidationError("Title should Have more characters")

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']              