from rest_framework import serializers
from .models import *

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostSerializerWithAllFields(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username')
    author_image = serializers.CharField(source='author.profile_img')
    class Meta:
        model = BlogPost
        fields = ['id','title','author_image','content','created_at','likes','is_blocked','image','comments','author_name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ExtraCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='user.username')
    author_image = serializers.CharField(source='user.profile_img')

    class Meta:
        model = Comment
        fields = ['author_name','author_image','text','created_at','post']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'