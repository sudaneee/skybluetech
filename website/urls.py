"""
URL configuration for the website app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Robots.txt
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # Core pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),

    # Products
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Services
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),

    # Team
    path('team/', views.TeamListView.as_view(), name='team'),

    # Clients
    path('clients/', views.ClientListView.as_view(), name='clients'),

    # Careers
    path('careers/', views.CareerListView.as_view(), name='careers'),
    path('careers/<slug:slug>/', views.CareerDetailView.as_view(), name='career_detail'),

    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/category/<slug:slug>/', views.BlogCategoryView.as_view(), name='blog_category'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),

    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),

    # Legal
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),

    # Newsletter
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),

    # 404 test page (development only)
    path('404/', views.Custom404View.as_view(), name='custom_404'),
]
