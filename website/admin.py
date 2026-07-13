"""
Customized Django admin for Skyblue Technology.

Features:
- Custom AdminSite with Skyblue branding
- Dashboard cards on the admin index
- Inline admins for related models
- Image previews, search, filters, ordering
- Bulk actions (activate/deactivate/soft delete)
- Collapsible fieldsets
- Automatic slug generation
"""

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import render
from django.db.models import Count

from .models import (
    SiteSettings, HeroSection, About, Mission, Vision, Values,
    WhyChooseUs, Product, ProductFeature, Service, ServiceFeature,
    Project, ProjectImage, ProjectTechnology, TeamMember, TeamSkill,
    Client, Testimonial, BlogCategory, BlogTag, BlogPost, Gallery,
    ContactInformation, SocialMedia, FAQs, Career, JobOpening,
    Newsletter, VisitorCounter, SiteSEO, ContactMessage,
    PrivacyPolicy, TermsOfService
)


# -----------------------------------------------------------------------------
# Admin Site Customization
# -----------------------------------------------------------------------------

class SkyblueAdminSite(admin.AdminSite):
    """Custom admin site with Skyblue Technology branding."""
    site_header = 'Skyblue Technology Administration'
    site_title = 'Skyblue Technology Admin'
    index_title = 'Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self._dashboard_stats())
        return super().index(request, extra_context=extra_context)

    def dashboard_view(self, request):
        context = {
            **self.each_context(request),
            **self._dashboard_stats(),
            'title': 'Dashboard',
        }
        return render(request, 'admin/dashboard.html', context)

    def _dashboard_stats(self):
        return {
            'product_count': Product.objects.filter(is_deleted=False).count(),
            'service_count': Service.objects.filter(is_deleted=False).count(),
            'project_count': Project.objects.filter(is_deleted=False).count(),
            'blog_count': BlogPost.objects.filter(is_deleted=False).count(),
            'job_count': JobOpening.objects.filter(is_deleted=False).count(),
            'message_count': ContactMessage.objects.filter(is_read=False).count(),
            'subscriber_count': Newsletter.objects.filter(is_active=True).count(),
            'visitor_count': VisitorCounter.objects.count(),
        }


admin_site = SkyblueAdminSite(name='skyblue_admin')


# -----------------------------------------------------------------------------
# Reusable Mixins
# -----------------------------------------------------------------------------

class SoftDeleteAdminMixin:
    """Mixin adding soft-delete bulk actions and filtering."""

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)

    actions = ['make_active', 'make_inactive', 'soft_delete_selected']

    @admin.action(description='Mark selected items as active')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected items as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Soft delete selected items')
    def soft_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.soft_delete()


class ImagePreviewMixin:
    """Mixin adding image preview readonly field."""

    def image_preview(self, obj):
        image_field = getattr(obj, 'image', None) or getattr(obj, 'logo', None) or \
                      getattr(obj, 'photo', None) or getattr(obj, 'cover_image', None) or \
                      getattr(obj, 'featured_image', None)
        if image_field:
            return mark_safe(f'<img src="{image_field.url}" style="max-height:80px;max-width:150px;border-radius:8px;" />')
        return '-'
    image_preview.short_description = 'Preview'


# -----------------------------------------------------------------------------
# Inline Admins
# -----------------------------------------------------------------------------

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    ordering = ['order']


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    ordering = ['order']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    ordering = ['order']


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1


class TeamSkillInline(admin.TabularInline):
    model = TeamSkill
    extra = 1


# -----------------------------------------------------------------------------
# Model Admin Configurations
# -----------------------------------------------------------------------------

@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Brand Identity', {
            'fields': ('site_name', 'tagline', 'logo', 'favicon'),
        }),
        ('Contact Defaults', {
            'fields': ('contact_email', 'contact_phone', 'address', 'working_hours'),
        }),
        ('Footer & Analytics', {
            'fields': ('footer_text', 'copyright_text', 'analytics_id', 'show_newsletter'),
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSection, site=admin_site)
class HeroSectionAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('headline', 'cta_text', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('headline', 'subheadline')
    list_editable = ('is_active', 'order')


@admin.register(About, site=admin_site)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'image'),
        }),
        ('Statistics', {
            'fields': (
                'years_experience', 'clients_served',
                'projects_completed', 'countries_served'
            ),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Mission, site=admin_site)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(Vision, site=admin_site)
class VisionAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(Values, site=admin_site)
class ValuesAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(WhyChooseUs, site=admin_site)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(Product, site=admin_site)
class ProductAdmin(SoftDeleteAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_featured', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'description')
    list_editable = ('is_featured', 'is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductFeatureInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description'),
        }),
        ('Media & Branding', {
            'fields': ('image', 'icon'),
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active', 'order'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Service, site=admin_site)
class ServiceAdmin(SoftDeleteAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_featured', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'description')
    list_editable = ('is_featured', 'is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceFeatureInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description'),
        }),
        ('Media & Branding', {
            'fields': ('image', 'icon'),
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active', 'order'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Project, site=admin_site)
class ProjectAdmin(SoftDeleteAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'status', 'is_featured', 'is_active', 'image_preview')
    list_filter = ('status', 'is_active', 'is_featured', 'category', 'completion_date')
    search_fields = ('title', 'client', 'description')
    list_editable = ('status', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, ProjectTechnologyInline]
    date_hierarchy = 'completion_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'client', 'category', 'description'),
        }),
        ('Media', {
            'fields': ('cover_image',),
        }),
        ('Status & Date', {
            'fields': ('status', 'completion_date', 'is_featured', 'is_active', 'order'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )


@admin.register(TeamMember, site=admin_site)
class TeamMemberAdmin(SoftDeleteAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('name', 'role', 'is_executive', 'is_active', 'order', 'image_preview')
    list_filter = ('is_executive', 'is_active', 'created_at')
    search_fields = ('name', 'role', 'biography')
    list_editable = ('is_executive', 'is_active', 'order')
    inlines = [TeamSkillInline]
    fieldsets = (
        ('Profile', {
            'fields': ('name', 'role', 'photo', 'biography'),
        }),
        ('Contact & Social', {
            'fields': ('email', 'phone', 'linkedin', 'facebook', 'twitter', 'instagram'),
        }),
        ('Visibility', {
            'fields': ('is_executive', 'is_active', 'order'),
        }),
    )


@admin.register(Client, site=admin_site)
class ClientAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('name', 'website', 'is_featured', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name',)
    list_editable = ('is_featured', 'is_active', 'order')


@admin.register(Testimonial, site=admin_site)
class TestimonialAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('author_name', 'company', 'rating', 'is_active', 'order')
    list_filter = ('rating', 'is_active')
    search_fields = ('author_name', 'company', 'comment')
    list_editable = ('is_active', 'order')


@admin.register(BlogCategory, site=admin_site)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogTag, site=admin_site)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost, site=admin_site)
class BlogPostAdmin(SoftDeleteAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'is_featured', 'views', 'published_at', 'image_preview')
    list_filter = ('is_published', 'is_featured', 'category', 'published_at')
    search_fields = ('title', 'content', 'excerpt', 'author')
    list_editable = ('is_published', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'tags', 'author', 'excerpt', 'content'),
        }),
        ('Media', {
            'fields': ('featured_image',),
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_at', 'views'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Gallery, site=admin_site)
class GalleryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'caption', 'is_active', 'order', 'image_preview')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'caption')


@admin.register(ContactInformation, site=admin_site)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('label', 'type', 'value', 'is_primary', 'is_active', 'order')
    list_filter = ('type', 'is_primary', 'is_active')
    list_editable = ('is_primary', 'is_active', 'order')
    search_fields = ('label', 'value')


@admin.register(SocialMedia, site=admin_site)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'order')
    list_filter = ('platform', 'is_active')
    list_editable = ('is_active', 'order')


@admin.register(FAQs, site=admin_site)
class FAQsAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('is_active', 'order')


@admin.register(Career, site=admin_site)
class CareerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Career Page', {
            'fields': ('title', 'content'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(JobOpening, site=admin_site)
class JobOpeningAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'type', 'is_active', 'posted_at', 'closes_at')
    list_filter = ('type', 'is_active', 'posted_at')
    search_fields = ('title', 'description', 'requirements')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'posted_at'
    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'slug', 'department', 'location', 'type'),
        }),
        ('Content', {
            'fields': ('description', 'requirements', 'benefits'),
        }),
        ('Publishing', {
            'fields': ('is_active', 'posted_at', 'closes_at'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Newsletter, site=admin_site)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    actions = ['activate_subscribers', 'deactivate_subscribers']

    @admin.action(description='Activate selected subscribers')
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected subscribers')
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(VisitorCounter, site=admin_site)
class VisitorCounterAdmin(admin.ModelAdmin):
    list_display = ('page_path', 'session_key', 'visited_at')
    list_filter = ('page_path', 'visited_at')
    readonly_fields = ('page_path', 'session_key', 'ip_hash', 'visited_at')

    def has_add_permission(self, request):
        return False


@admin.register(SiteSEO, site=admin_site)
class SiteSEOAdmin(admin.ModelAdmin):
    list_display = ('page_path', 'meta_title', 'canonical_url')
    search_fields = ('page_path', 'meta_title', 'meta_description')


@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)


@admin.register(PrivacyPolicy, site=admin_site)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Privacy Policy', {
            'fields': ('title', 'content', 'last_updated'),
        }),
    )
    readonly_fields = ('last_updated', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TermsOfService, site=admin_site)
class TermsOfServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Terms of Service', {
            'fields': ('title', 'content', 'last_updated'),
        }),
    )
    readonly_fields = ('last_updated', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# -----------------------------------------------------------------------------
# Default Django Admin Registration
# -----------------------------------------------------------------------------
# Also register models with the default admin for compatibility during setup.
# The custom admin_site above is the primary interface.

models_to_register = [
    SiteSettings, HeroSection, About, Mission, Vision, Values,
    WhyChooseUs, Product, ProductFeature, Service, ServiceFeature,
    Project, ProjectImage, ProjectTechnology, TeamMember, TeamSkill,
    Client, Testimonial, BlogCategory, BlogTag, BlogPost, Gallery,
    ContactInformation, SocialMedia, FAQs, Career, JobOpening,
    Newsletter, VisitorCounter, SiteSEO, ContactMessage,
    PrivacyPolicy, TermsOfService
]

for model in models_to_register:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
