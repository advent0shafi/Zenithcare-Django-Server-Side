from django.shortcuts import render
from rest_framework import generics
from .models import BlogPost,Like,Comment
from .serializers import BlogPostSerializer,BlogPostSerializerWithAllFields,LikeSerializer,CommentSerializer,ExtraCommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from authentification.models import User

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostDetailView(generics.ListAPIView):
    serializer_class = BlogPostSerializerWithAllFields

    def get_queryset(self):
        author_id = self.kwargs['pk']
        return BlogPost.objects.filter(author=author_id)


class BlogPostFullDetailView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializerWithAllFields
    def get_queryset(self):
        return BlogPost.objects.all()


class BlogPostDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeCountView(APIView):
    def get(self, request, pk):
        blog = BlogPost.objects.get(id=pk)
        like_count = Like.objects.filter(blog=blog).count()
        return Response({"like_count": like_count})
    


class LikeView(APIView):
    def post(self, request, pk):
        try:
            user_id = request.data.get('userId', None)
            user = User.objects.get(id=user_id)
            blog_post = BlogPost.objects.get(id=pk)
            like, created = Like.objects.get_or_create(user=user, blog=blog_post)
            if created:
                return Response({'message': 'Blog post liked!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'You have already liked this blog post.'}, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'message': 'Blog post not found.'}, status=status.HTTP_404_NOT_FOUND)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = ExtraCommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Comment.objects.filter(post__id=post_id)



class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
