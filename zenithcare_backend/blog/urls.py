from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [ 
 path('blogcreate', BlogPostListCreateView.as_view(), name='blogpost-list-create'),
 path('bloglist/<int:pk>', BlogPostDetailView.as_view(), name='blogpost-detail'),
 path('blog-delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost-delete'),
 path('blogposts/', BlogPostFullDetailView.as_view(), name='blogpost-list'),
 path('likes/', LikeListCreateView.as_view(), name='like-list-create'),
 path('blog-likes/<int:pk>/', LikeCountView.as_view(), name='blog-like'),
path('like/<int:pk>/', LikeView.as_view(), name='like-blog-post'),
path('blog-comments/<int:pk>/', CommentListCreateView.as_view(), name='blog-comments'),
path('comment-create/', CommentCreateView.as_view(), name='comment-create'),

]   

