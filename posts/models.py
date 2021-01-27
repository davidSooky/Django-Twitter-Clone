from django.db import models
from user.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

#Model for creating tweets
class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tweets")
    title = models.CharField(max_length=400)
    content = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def num_of_likes(self):
        return self.likes.count()

    @property
    def username(self):
        return self.owner.user.username

    @property
    def num_of_comments(self):
        return self.comments.count()
    
    def __str__(self):
        return self.title[:10]

    def get_absolute_url(self):
        return reverse("posts:comments", kwargs={"pk":self.id})

    class Meta:
        ordering = ["-created_on"]

#Model for creating comments
class Comment(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:10]

    @property
    def username(self):
        return self.owner.user.username

    class Meta:
        ordering = ["-updated_on"]

#Model for likes
class Like(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ["owner", "post"]

    def save(self, *args, **kwargs):
        if self.owner == self.post.owner:
            return None
        super().save(*args, **kwargs)