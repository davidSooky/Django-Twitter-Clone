from django import template
from posts.models import Like
from user.models import Profile, Follower

register = template.Library()

@register.simple_tag()
def already_liked(post_id, user_id):    
    """
    Django template tag to determine whether 
    a post is already liked by current user
    :param post_id: id of the specific post
    :param user_id: id of current user
    """

    profile = Profile.objects.get(user=user_id)
    try:
        like = Like.objects.get(post=post_id, owner=profile)
        return True
    except Like.DoesNotExist:
        return False

@register.simple_tag()
def is_followed(owner_id, follower_id):
    """
    Django template tag to determine whether 
    a profile is followed by current user
    :param follower_id: id of the showed profile
    :param owner_id: id of current user
    """

    try:
        follower = Follower.objects.get(owner_id=owner_id, follower_id=follower_id)
        return True
    except Follower.DoesNotExist:
        return False

@register.filter
def format_number(value, num_decimals=2):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    int_value = int(value)
    formatted_number = '{{:.{}f}}'.format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value/1000.0).rstrip('0.') + 'K'
    else:
        return formatted_number.format(int_value/1000000.0).rstrip('0.') + 'M'