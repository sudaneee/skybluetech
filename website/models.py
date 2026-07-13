"""
Models for the Skyblue Technology corporate website.

All website content is database-driven. No hardcoded text should appear in
views or templates; everything is editable through the Django admin.
"""

import os
import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

def upload_path(instance, filename, folder):
    """Generate a clean upload path with UUID filename."""
    ext = filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(folder, filename)


def site_logo_path(instance, filename):
    return upload_path(instance, filename, 'site/logo')


def site_favicon_path(instance, filename):
    return upload_path(instance, filename, 'site/favicon')


def hero_image_path(instance, filename):
    return upload_path(instance, filename, 'hero')


def product_image_path(instance, filename):
    return upload_path(instance, filename, 'products')


def service_image_path(instance, filename):
    return upload_path(instance, filename, 'services')


def project_image_path(instance, filename):
    return upload_path(instance, filename, 'projects')


def team_image_path(instance, filename):
    return upload_path(instance, filename, 'team')


def client_logo_path(instance, filename):
    return upload_path(instance, filename, 'clients')


def blog_image_path(instance, filename):
    return upload_path(instance, filename, 'blog')


def testimonial_image_path(instance, filename):
    return upload_path(instance, filename, 'testimonials')


def gallery_image_path(instance, filename):
    return upload_path(instance, filename, 'gallery')


def og_image_path(instance, filename):
    return upload_path(instance, filename, 'seo')


def about_image_path(instance, filename):
    return upload_path(instance, filename, 'about')


# -----------------------------------------------------------------------------
# Abstract Base Models
# -----------------------------------------------------------------------------

class TimestampModel(models.Model):
    """Adds created_at and updated_at timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Adds soft-delete support."""
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])


class OrderedModel(models.Model):
    """Adds an order field for manual sorting."""
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order', '-created_at']


class SEOModel(models.Model):
    """Adds SEO fields to models that need per-object SEO control."""
    meta_title = models.CharField(
        max_length=255, blank=True,
        help_text="Override default meta title."
    )
    meta_description = models.TextField(
        blank=True,
        help_text="Override default meta description."
    )
    meta_keywords = models.CharField(
        max_length=500, blank=True,
        help_text="Comma-separated keywords."
    )

    class Meta:
        abstract = True


# -----------------------------------------------------------------------------
# Singleton Mixin
# -----------------------------------------------------------------------------

class SingletonModel(models.Model):
    """Ensures only one instance of the model exists."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


# -----------------------------------------------------------------------------
# Site Configuration
# -----------------------------------------------------------------------------

class SiteSettings(SingletonModel, TimestampModel):
    """Global website settings."""
    site_name = models.CharField(max_length=100, default='Skyblue Technology')
    tagline = models.CharField(
        max_length=255,
        default='Innovative Technology Solutions for a Smarter Tomorrow'
    )
    logo = models.ImageField(
        upload_to=site_logo_path, blank=True, null=True,
        help_text='Recommended size: 240x80px transparent PNG.'
    )
    favicon = models.ImageField(
        upload_to=site_favicon_path, blank=True, null=True,
        help_text='Recommended size: 32x32px ICO or PNG.'
    )
    footer_text = models.TextField(
        blank=True,
        default='Delivering world-class technology solutions across education, healthcare, commerce, and financial services.'
    )
    copyright_text = models.CharField(
        max_length=255,
        default='© Skyblue Technology. All rights reserved.'
    )
    analytics_id = models.CharField(
        max_length=50, blank=True,
        help_text='Google Analytics 4 Measurement ID (G-XXXXXXXXXX).'
    )
    contact_email = models.EmailField(default='info@skybluetechnology.com')
    contact_phone = models.CharField(max_length=50, default='+234 000 000 0000')
    address = models.TextField(
        default='Skyblue Technology Headquarters, Nigeria'
    )
    working_hours = models.CharField(
        max_length=255, default='Monday - Friday: 9:00 AM - 5:00 PM'
    )
    show_newsletter = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name


# -----------------------------------------------------------------------------
# Hero Section
# -----------------------------------------------------------------------------

class HeroSection(TimestampModel):
    """Homepage hero slides."""
    headline = models.CharField(max_length=200)
    subheadline = models.TextField(
        blank=True,
        help_text='Short description below the headline.'
    )
    background_image = models.ImageField(
        upload_to=hero_image_path, blank=True, null=True
    )
    background_video = models.URLField(
        blank=True,
        help_text='Optional YouTube/Vimeo background video URL.'
    )
    cta_text = models.CharField(max_length=50, default='Get Started')
    cta_url = models.CharField(max_length=255, default='/contact/')
    secondary_cta_text = models.CharField(max_length=50, blank=True)
    secondary_cta_url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.headline


# -----------------------------------------------------------------------------
# About, Mission, Vision, Values
# -----------------------------------------------------------------------------

class About(SingletonModel, TimestampModel):
    """Company overview content."""
    title = models.CharField(max_length=200, default='About Skyblue Technology')
    content = CKEditor5Field(
        'Company Overview',
        config_name='default',
        default='<p>Skyblue Technology is a leading technology company...</p>'
    )
    years_experience = models.PositiveIntegerField(default=10)
    clients_served = models.PositiveIntegerField(default=500)
    projects_completed = models.PositiveIntegerField(default=1200)
    countries_served = models.PositiveIntegerField(default=5)
    image = models.ImageField(
        upload_to=about_image_path,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return self.title


class Mission(TimestampModel, OrderedModel):
    """Mission cards."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, default='bi-bullseye',
        help_text='Bootstrap Icons class, e.g., bi-bullseye'
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Mission'
        verbose_name_plural = 'Mission Statements'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Vision(TimestampModel, OrderedModel):
    """Vision cards."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, default='bi-eye',
        help_text='Bootstrap Icons class, e.g., bi-eye'
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Vision'
        verbose_name_plural = 'Vision Statements'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class Values(TimestampModel, OrderedModel):
    """Core values cards."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, default='bi-heart',
        help_text='Bootstrap Icons class, e.g., bi-heart'
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Core Value'
        verbose_name_plural = 'Core Values'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# Why Choose Us
# -----------------------------------------------------------------------------

class WhyChooseUs(TimestampModel, OrderedModel):
    """Reasons to choose Skyblue Technology."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, default='bi-check-circle',
        help_text='Bootstrap Icons class.'
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Why Choose Us'
        verbose_name_plural = 'Why Choose Us'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# Products
# -----------------------------------------------------------------------------

class Product(TimestampModel, SEOModel, SoftDeleteModel):
    """Products offered by Skyblue Technology."""
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    short_description = models.TextField(
        help_text='Brief summary shown on listing pages.'
    )
    description = CKEditor5Field(config_name='default')
    image = models.ImageField(
        upload_to=product_image_path, blank=True, null=True
    )
    icon = models.CharField(
        max_length=50, default='bi-box-seam',
        help_text='Bootstrap Icons class.'
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class ProductFeature(TimestampModel, OrderedModel):
    """Features belonging to a product."""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='features'
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50, default='bi-check-lg',
        help_text='Bootstrap Icons class.'
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.product.title} - {self.name}"


# -----------------------------------------------------------------------------
# Services
# -----------------------------------------------------------------------------

class Service(TimestampModel, SEOModel, SoftDeleteModel):
    """Services offered by Skyblue Technology."""
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    short_description = models.TextField()
    description = CKEditor5Field(config_name='default')
    image = models.ImageField(
        upload_to=service_image_path, blank=True, null=True
    )
    icon = models.CharField(
        max_length=50, default='bi-gear',
        help_text='Bootstrap Icons class.'
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class ServiceFeature(TimestampModel, OrderedModel):
    """Features belonging to a service."""
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='features'
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50, default='bi-check-lg',
        help_text='Bootstrap Icons class.'
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Service Feature'
        verbose_name_plural = 'Service Features'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.service.title} - {self.name}"


# -----------------------------------------------------------------------------
# Projects
# -----------------------------------------------------------------------------

class Project(TimestampModel, SEOModel, SoftDeleteModel):
    """Portfolio projects."""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    client = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, blank=True)
    description = CKEditor5Field(config_name='default')
    cover_image = models.ImageField(
        upload_to=project_image_path, blank=True, null=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='completed'
    )
    completion_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['order', '-completion_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class ProjectImage(TimestampModel, OrderedModel):
    """Gallery images for a project."""
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='gallery_images'
    )
    image = models.ImageField(upload_to=project_image_path)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Image'}"


class ProjectTechnology(TimestampModel):
    """Technologies used in a project."""
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='technologies'
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Project Technology'
        verbose_name_plural = 'Project Technologies'

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# Team
# -----------------------------------------------------------------------------

class TeamMember(TimestampModel, SoftDeleteModel):
    """Team members and executives."""
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to=team_image_path, blank=True, null=True
    )
    biography = CKEditor5Field(config_name='default', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    is_executive = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"

    def get_absolute_url(self):
        return reverse('team')


class TeamSkill(TimestampModel):
    """Skills for a team member."""
    member = models.ForeignKey(
        TeamMember, on_delete=models.CASCADE, related_name='skills'
    )
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Proficiency percentage from 0 to 100.'
    )

    class Meta:
        verbose_name = 'Team Skill'
        verbose_name_plural = 'Team Skills'

    def __str__(self):
        return f"{self.member.name} - {self.name}"


# -----------------------------------------------------------------------------
# Clients & Testimonials
# -----------------------------------------------------------------------------

class Client(TimestampModel):
    """Client companies / logo carousel."""
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to=client_logo_path)
    website = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name


class Testimonial(TimestampModel):
    """Customer testimonials."""
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='testimonials'
    )
    author_name = models.CharField(max_length=150)
    author_title = models.CharField(max_length=150, blank=True)
    author_photo = models.ImageField(
        upload_to=testimonial_image_path, blank=True, null=True
    )
    company = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.company or 'Skyblue Technology'}"


# -----------------------------------------------------------------------------
# Blog
# -----------------------------------------------------------------------------

class BlogCategory(TimestampModel):
    """Blog post categories."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})


class BlogTag(TimestampModel):
    """Tags for blog posts."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimestampModel, SEOModel, SoftDeleteModel):
    """Blog articles."""
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    author = models.CharField(max_length=150, default='Skyblue Technology')
    featured_image = models.ImageField(
        upload_to=blog_image_path, blank=True, null=True
    )
    excerpt = models.TextField(
        blank=True,
        help_text='Short summary for listing pages.'
    )
    content = CKEditor5Field(config_name='default')
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


# -----------------------------------------------------------------------------
# Gallery
# -----------------------------------------------------------------------------

class Gallery(TimestampModel, OrderedModel):
    """General image gallery."""
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=gallery_image_path)
    caption = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# Contact & Social
# -----------------------------------------------------------------------------

class ContactInformation(TimestampModel, OrderedModel):
    """Contact details (address, phone, email)."""
    INFO_TYPES = [
        ('address', 'Address'),
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('working_hours', 'Working Hours'),
    ]

    type = models.CharField(max_length=20, choices=INFO_TYPES, db_index=True)
    label = models.CharField(max_length=100)
    value = models.TextField()
    icon = models.CharField(
        max_length=50, default='bi-geo-alt',
        help_text='Bootstrap Icons class.'
    )
    is_primary = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.label} ({self.get_type_display()})"


class SocialMedia(TimestampModel, OrderedModel):
    """Social media links."""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('github', 'GitHub'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(
        max_length=50, blank=True,
        help_text='Optional Bootstrap Icons class override.'
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.get_platform_display()


# -----------------------------------------------------------------------------
# FAQs
# -----------------------------------------------------------------------------

class FAQs(TimestampModel, OrderedModel):
    """Frequently asked questions."""
    category = models.CharField(max_length=100, blank=True, db_index=True)
    question = models.CharField(max_length=255)
    answer = CKEditor5Field(config_name='default')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.question


# -----------------------------------------------------------------------------
# Careers
# -----------------------------------------------------------------------------

class Career(SingletonModel, TimestampModel):
    """Careers page content."""
    title = models.CharField(
        max_length=200, default='Careers at Skyblue Technology'
    )
    content = CKEditor5Field(
        config_name='default',
        default='<p>Join our team of innovators...</p>'
    )

    class Meta:
        verbose_name = 'Career Page'
        verbose_name_plural = 'Career Page'

    def __str__(self):
        return self.title


class JobOpening(TimestampModel, SEOModel, SoftDeleteModel):
    """Job openings / vacancies."""
    JOB_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, default='Nigeria')
    type = models.CharField(
        max_length=20, choices=JOB_TYPES, default='full_time'
    )
    description = CKEditor5Field(config_name='default')
    requirements = CKEditor5Field(config_name='default')
    benefits = CKEditor5Field(config_name='default', blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    posted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    closes_at = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Job Opening'
        verbose_name_plural = 'Job Openings'
        ordering = ['-posted_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('career_detail', kwargs={'slug': self.slug})


# -----------------------------------------------------------------------------
# Newsletter
# -----------------------------------------------------------------------------

class Newsletter(TimestampModel):
    """Newsletter subscribers."""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True, db_index=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


# -----------------------------------------------------------------------------
# Visitor Counter
# -----------------------------------------------------------------------------

class VisitorCounter(models.Model):
    """Simple page visit tracker."""
    page_path = models.CharField(max_length=255, db_index=True)
    session_key = models.CharField(max_length=255, blank=True, db_index=True)
    ip_hash = models.CharField(max_length=64, blank=True, db_index=True)
    visited_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Visitor Counter'
        verbose_name_plural = 'Visitor Counters'
        ordering = ['-visited_at']

    def __str__(self):
        return f"{self.page_path} at {self.visited_at}"


# -----------------------------------------------------------------------------
# Site SEO
# -----------------------------------------------------------------------------

class SiteSEO(TimestampModel):
    """Per-page SEO overrides."""
    page_path = models.CharField(
        max_length=255, unique=True, db_index=True,
        help_text='URL path, e.g., /about/ or /products/skycollect/'
    )
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    og_image = models.ImageField(
        upload_to=og_image_path, blank=True, null=True
    )
    canonical_url = models.URLField(blank=True)
    schema_markup = models.JSONField(
        blank=True, null=True,
        help_text='Optional JSON-LD Schema.org markup.'
    )

    class Meta:
        verbose_name = 'Site SEO'
        verbose_name_plural = 'Site SEO Entries'

    def __str__(self):
        return self.page_path


# -----------------------------------------------------------------------------
# Contact Messages
# -----------------------------------------------------------------------------

class ContactMessage(TimestampModel):
    """Messages submitted via the contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


# -----------------------------------------------------------------------------
# Legal Pages
# -----------------------------------------------------------------------------

class PrivacyPolicy(SingletonModel, TimestampModel):
    """Privacy policy page content."""
    title = models.CharField(max_length=200, default='Privacy Policy')
    content = CKEditor5Field(
        config_name='default',
        default='<p>Your privacy is important to us...</p>'
    )
    last_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policy'

    def __str__(self):
        return self.title


class TermsOfService(SingletonModel, TimestampModel):
    """Terms of service page content."""
    title = models.CharField(max_length=200, default='Terms of Service')
    content = CKEditor5Field(
        config_name='default',
        default='<p>These terms govern your use of our services...</p>'
    )
    last_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Terms of Service'
        verbose_name_plural = 'Terms of Service'

    def __str__(self):
        return self.title
