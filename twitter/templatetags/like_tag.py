from django import template

from twitter.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def is_like(context, post_id):
    request = context['request']

    try:
        post_likes = PostLike.objects.get(post__id=post_id, liked_by=request.user.id).is_like
    except Exception as ex:
        post_likes = False

    return post_likes

@register.simple_tag()
def count_likes(post_id):
    return PostLike.objects.filter(post__id=post_id, is_like=True).count()

@register.simple_tag(takes_context=True)
def post_likes_id(context, post_id):
    request = context['request']
    return PostLike.objects.get(post__id=post_id, liked_by=request.user.id).pk