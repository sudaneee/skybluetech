"""
Root URL configuration for Skyblue Technology.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from website.admin import admin_site
from website.sitemaps import (
    StaticViewSitemap,
    ProductSitemap,
    ServiceSitemap,
    ProjectSitemap,
    BlogPostSitemap,
    JobOpeningSitemap,
)

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'services': ServiceSitemap,
    'projects': ProjectSitemap,
    'blog': BlogPostSitemap,
    'careers': JobOpeningSitemap,
}

urlpatterns = [
    path('admin/', admin_site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('website.urls')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'website.views.custom_404_handler'
handler500 = 'website.views.custom_500_handler'
