from .models import Profile
from random import choice

def get_followed_users(profile):
    '''
    Function to get profile_ID of all the followed users
    plust the currently logged in user:
    params:
        profile: profile of currently logged in user
    '''
    followed_users = [*profile.following.all().values_list("follower_id", flat=True).distinct()]
    followed_users.append(profile.id)
    return followed_users

def get_recommended_users(profile):
    '''
    Function to get profile_ID of all the followed users
    plust the currently logged in user:
    params:
        profile: profile of currently logged in user
    '''
    followed_users = get_followed_users(profile)
    non_followed_users = Profile.objects.all().exclude(id__in=followed_users)

    if len(non_followed_users) <= 3:
        return non_followed_users
    else:
        users = []
        while len(users) < 3:
            user = choice(non_followed_users)
            if user not in users:
                users.append(user)
        return users