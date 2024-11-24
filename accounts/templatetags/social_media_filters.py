from django import template

register = template.Library()

@register.filter(name='add_social_media_url')
def add_social_media_url(user_id, social_media):
    urls = {
        'facebook': 'https://www.facebook.com/',
        'instagram': 'https://www.instagram.com/',
        'twitter': 'https://twitter.com/',
        'linkedin': 'https://www.linkedin.com/in/',
        'youtube': 'https://www.youtube.com/user/',
        'telegram': 'https://t.me/',
        'vk': 'https://vk.com/',
        'tiktok': 'https://www.tiktok.com/@',
    }
    return urls.get(social_media, '') + user_id
