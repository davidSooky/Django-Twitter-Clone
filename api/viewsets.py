from .serializers import PostSerializer, LikeSerializer, FollowerSerializer, PostDetailSerializer, ProfileSerializer
from posts.models import Post, Like
from user.models import Profile, Follower
from user.utils import get_followed_users

# Third party imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

@api_view(['GET'])
def post_all(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def users_posts(request, pk):
    posts = Post.objects.filter(owner_id=pk)
    serializer = PostDetailSerializer(posts, many=True, context = {'request':request})

    return Response(serializer.data)

@api_view(['GET'])
def followed_users_posts(request, pk):
    user = Profile.objects.get(pk=pk)
    posts = Post.objects.filter(owner_id__in=get_followed_users(user)).order_by("-created_on")
    serializer = PostDetailSerializer(posts, many=True, context = {'request':request})

    return Response(serializer.data)

@api_view(['GET'])
def users(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def create_like(request):
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def delete_like(request, pk):
    user = Profile.objects.get(user=request.user)
    like = Like.objects.filter(owner=user.id).filter(post=pk)
    like.delete()
    return Response("Like deleted.")

@api_view(['POST'])
def create_follower(request):
    serializer = FollowerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def delete_follower(request, pk):
    user = Profile.objects.get(user=request.user)
    follower = Follower.objects.filter(owner_id=user.id).filter(follower_id=pk)
    follower.delete()
    return Response("Follower deleted.")