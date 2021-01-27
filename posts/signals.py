from django.db.models.signals import pre_save
from .models import Comment

def create_comment(sender, instance, **kwargs):
    profile = kwargs.get("profile")
    post = kwargs.get("post")
    Comment.objects.create(owner=profile, post=post)

pre_save.connect(create_comment, sender=Comment)