"""
Sitemap definitions for Skyblue Technology.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product, Service, Project, BlogPost, JobOpening


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'about',
            'products',
            'services',
            'projects',
            'team',
            'clients',
            'careers',
            'blog',
            'contact',
            'privacy_policy',
            'terms_of_service',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    """Sitemap for products."""
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Product.objects.filter(is_active=True, is_deleted=False)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    """Sitemap for services."""
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Service.objects.filter(is_active=True, is_deleted=False)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    """Sitemap for projects."""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return Project.objects.filter(is_active=True, is_deleted=False)

    def lastmod(self, obj):
        return obj.updated_at


class BlogPostSitemap(Sitemap):
    """Sitemap for blog posts."""
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return BlogPost.objects.filter(is_published=True, is_deleted=False)

    def lastmod(self, obj):
        return obj.updated_at


class JobOpeningSitemap(Sitemap):
    """Sitemap for job openings."""
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return JobOpening.objects.filter(is_active=True, is_deleted=False)

    def lastmod(self, obj):
        return obj.updated_at
