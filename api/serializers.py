from rest_framework import serializers
from posts.models import Post, Like
from user.models import Follower, Profile

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "profile_pic", "username", "absolute_url"]


class PostDetailSerializer(serializers.ModelSerializer):
    already_liked = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True, source="owner")
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "tweet_image", "owner", "num_of_likes", "num_of_comments", "absolute_url", "created_on", "already_liked", "profile"]

    def get_already_liked(self, obj):
        user = self.context["request"].user
        profile = Profile.objects.get(user__username=user).id

        return Like.objects.filter(post=obj.id, owner=profile).exists()