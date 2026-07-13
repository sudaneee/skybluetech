"""
Custom template tags and filters for Skyblue Technology.
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Access dictionary value by key in templates."""
    return dictionary.get(key)


@register.filter
def stars(rating):
    """Render Bootstrap star icons for a numeric rating."""
    full = int(rating)
    empty = 5 - full
    html = ''
    for _ in range(full):
        html += '<i class="bi bi-star-fill text-warning"></i>'
    for _ in range(empty):
        html += '<i class="bi bi-star text-warning"></i>'
    return mark_safe(html)


@register.simple_tag
def active_class(request, url_name):
    """Return 'active' if current path matches the named URL."""
    from django.urls import reverse
    try:
        if request.path == reverse(url_name):
            return 'active'
    except Exception:
        pass
    return ''


@register.simple_tag(takes_context=True)
def placeholder_image(context, width=600, height=400, text=''):
    """Return a placeholder image URL."""
    label = text or 'Skyblue'
    return f"https://placehold.co/{width}x{height}/0d6efd/ffffff?text={label}"
