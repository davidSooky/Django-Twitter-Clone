from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from PIL import Image
# Create your models here.

# Specifies save path for images for each profile
def get_prof_path_name(instance, filename):
    return "/".join(['images', instance.user.username, "profile", filename])

def get_cover_path_name(instance, filename):
    return "/".join(['images', instance.user.username, "cover", filename])


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(default="images/default_profile.jpg", upload_to=get_prof_path_name)
    cover_pic = models.ImageField(default="images/default_cover.jpg", upload_to=get_cover_path_name)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    # description = models.CharField(max_length=300, blank=True, null=True)
    # country = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=100)
    # dob = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("user:profile", kwargs={"username":self.user})

    @property
    def num_of_followers(self):
        return self.followers.count()  

    @property
    def num_of_following(self):
        return self.following.count()

    @property
    def num_of_tweets(self):
        return self.tweets.count()  

    def __str__(self):
        if self.first_name:
            return str(f"{self.first_name} {self.last_name}")
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        prof_img = Image.open(self.profile_pic.path)
        cover_img = Image.open(self.cover_pic.path)
        if prof_img.width > 300 or prof_img.height > 300:
            output_size = (300, 300)   
            prof_img.thumbnail(output_size)
            prof_img.save(self.profile_pic.path)

        if cover_img.width > 1500 or cover_img.height > 500:
            output_size = (1500, 500)
            cover_img.thumbnail(output_size)
            cover_img.save(self.profile_pic.path)

class Follower(models.Model):
    owner_id = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    follower_id = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["owner_id", "follower_id"]

    def __str__(self):
        return str(f"{self.owner_id} - {self.follower_id}")