from django.db.models.signals import pre_delete
from .models import Post

# Signal to delete uploaded image, if tweet gets deleted
def delete_tweet_image(sender, instance, **kwargs):
    try:
        tweet = sender.objects.get(pk=instance.pk)
    except tweet.DoesNotExist:
        return False
    else:
        tweet_img = tweet.tweet_image
        tweet_img.delete()

pre_delete.connect(delete_tweet_image, sender=Post)