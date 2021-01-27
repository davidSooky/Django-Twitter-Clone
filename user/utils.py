
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