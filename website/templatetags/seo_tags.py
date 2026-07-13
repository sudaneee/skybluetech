"""
SEO helper template tags.
"""

from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def meta_title(context):
    """Resolve page meta title."""
    seo = context.get('seo')
    if seo and getattr(seo, 'meta_title', None):
        return seo.meta_title
    global_seo = context.get('global_seo')
    if isinstance(global_seo, dict):
        return global_seo.get('meta_title', '')
    return getattr(global_seo, 'meta_title', '')


@register.simple_tag(takes_context=True)
def meta_description(context):
    """Resolve page meta description."""
    seo = context.get('seo')
    if seo and getattr(seo, 'meta_description', None):
        return seo.meta_description
    global_seo = context.get('global_seo')
    if isinstance(global_seo, dict):
        return global_seo.get('meta_description', '')
    return getattr(global_seo, 'meta_description', '')


@register.simple_tag(takes_context=True)
def meta_keywords(context):
    """Resolve page meta keywords."""
    seo = context.get('seo')
    if seo and getattr(seo, 'keywords', None):
        return seo.keywords
    global_seo = context.get('global_seo')
    if isinstance(global_seo, dict):
        return global_seo.get('keywords', '')
    return getattr(global_seo, 'keywords', '')


@register.simple_tag(takes_context=True)
def canonical_url(context):
    """Return canonical URL for the current page."""
    request = context.get('request')
    seo = context.get('seo')
    if seo and getattr(seo, 'canonical_url', None):
        return seo.canonical_url
    if request:
        return request.build_absolute_uri()
    return ''


@register.simple_tag(takes_context=True)
def og_image_url(context):
    """Return Open Graph image URL."""
    seo = context.get('seo')
    if seo and getattr(seo, 'og_image', None):
        return context['request'].build_absolute_uri(seo.og_image.url)
    site_settings = context.get('site_settings')
    if site_settings and getattr(site_settings, 'logo', None):
        return context['request'].build_absolute_uri(site_settings.logo.url)
    return ''


@register.simple_tag(takes_context=True)
def organization_schema(context):
    """Render Schema.org Organization JSON-LD."""
    site = context.get('site_settings')
    if not site:
        return ''
    data = {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': site.site_name,
        'url': context.get('request').build_absolute_uri('/') if context.get('request') else '',
        'logo': context.get('request').build_absolute_uri(site.logo.url) if site.logo and context.get('request') else '',
        'description': site.tagline,
        'contactPoint': {
            '@type': 'ContactPoint',
            'telephone': site.contact_phone,
            'contactType': 'customer service',
            'email': site.contact_email,
        }
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')
