"""
Global context processors for Skyblue Technology.

These make site-wide data available in every template without repeating
queries in each view.
"""

from django.conf import settings

from .models import (
    SiteSettings, SiteSEO, Product, Service, SocialMedia,
    ContactInformation
)


def site_settings(request):
    """Inject global site settings into every template."""
    return {
        'site_settings': SiteSettings.load(),
    }


def global_seo(request):
    """Inject default SEO data into every template."""
    page_path = request.path
    try:
        seo = SiteSEO.objects.get(page_path=page_path)
    except SiteSEO.DoesNotExist:
        site = SiteSettings.load()
        seo = {
            'meta_title': f"{site.site_name} - {site.tagline}",
            'meta_description': site.tagline,
            'keywords': '',
            'og_image': None,
            'canonical_url': request.build_absolute_uri(page_path),
        }
    return {
        'global_seo': seo,
        'request_path': page_path,
    }


def navigation(request):
    """Inject navigation data into every template."""
    return {
        'nav_products': Product.objects.filter(
            is_active=True, is_deleted=False
        )[:6],
        'nav_services': Service.objects.filter(
            is_active=True, is_deleted=False
        )[:6],
    }


def footer_context(request):
    """Inject footer data into every template."""
    return {
        'footer_products': Product.objects.filter(
            is_active=True, is_deleted=False
        )[:5],
        'footer_services': Service.objects.filter(
            is_active=True, is_deleted=False
        )[:5],
        'footer_social': SocialMedia.objects.filter(is_active=True),
        'footer_contact': ContactInformation.objects.filter(is_active=True),
    }
