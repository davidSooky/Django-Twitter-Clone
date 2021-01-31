from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User

from .models import Profile

# Signal to automatically create a profile for the registered User
# def create_profile(sender, created, instance, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, email=instance.email)

# post_save.connect(create_profile, sender=User)

# def update_profile(sender, instance, **kwargs):
#     profile = sender.objects.get(pk=instance.pk)
#     profile.first_name = instance.first_name
#     profile.last_name = instance.last_name
#     profile.dob = instance.dob

# pre_save.connect(update_profile, sender=Profile)

# Signal to delete previous profile picture
def delete_old_prof_pictures(sender, instance, **kwargs):
    try:
        profile = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    old_prof_pic = profile.profile_pic
    new_prof_pic = instance.profile_pic
    
    if new_prof_pic and not new_prof_pic.path == old_prof_pic.path:
        old_prof_pic.delete(save=False)

# Signal to delete previous cover picture
def delete_old_cover_pictures(sender, instance, **kwargs):
    try:
        profile = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    old_cover_pic = profile.cover_pic
    new_cover_pic = instance.cover_pic

    if new_cover_pic and not new_cover_pic.path == old_cover_pic.path:
        old_cover_pic.delete(save=False)

pre_save.connect(delete_old_prof_pictures, sender=Profile)
pre_save.connect(delete_old_cover_pictures, sender=Profile)
