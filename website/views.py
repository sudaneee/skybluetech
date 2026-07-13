"""
Views for the Skyblue Technology corporate website.

All views pull content from the database. No hardcoded text is used.
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, View
)
from django.views.decorators.http import require_GET
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .models import (
    SiteSettings, HeroSection, About, Mission, Vision, Values,
    WhyChooseUs, Product, Service, Project, TeamMember, Client,
    Testimonial, BlogCategory, BlogPost, Gallery, ContactInformation,
    SocialMedia, FAQs, Career, JobOpening, Newsletter, SiteSEO,
    ContactMessage, PrivacyPolicy, TermsOfService, VisitorCounter
)
from .forms import ContactForm, NewsletterForm


# -----------------------------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------------------------

def custom_404_handler(request, exception=None):
    """Custom 404 error handler."""
    return render(request, 'website/pages/404.html', status=404)


def custom_500_handler(request):
    """Custom 500 error handler."""
    return HttpResponseServerError(render(request, '500.html').content)


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

def get_seo_context(page_path):
    """Fetch SEO data for a given page path."""
    try:
        return SiteSEO.objects.get(page_path=page_path)
    except SiteSEO.DoesNotExist:
        return None


def track_visitor(request, page_path):
    """Track page visits for analytics dashboard."""
    session_key = request.session.session_key or ''
    VisitorCounter.objects.create(
        page_path=page_path,
        session_key=session_key,
        ip_hash=''
    )


# -----------------------------------------------------------------------------
# Legal / Utility Views
# -----------------------------------------------------------------------------

@require_GET
def robots_txt(request):
    """Serve robots.txt."""
    lines = [
        'User-Agent: *',
        'Allow: /',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


class Custom404View(TemplateView):
    """Custom 404 page for development testing."""
    template_name = 'website/pages/404.html'


# -----------------------------------------------------------------------------
# Home Page
# -----------------------------------------------------------------------------

class HomeView(TemplateView):
    template_name = 'website/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_slides'] = HeroSection.objects.filter(is_active=True)
        context['about'] = About.load()
        context['missions'] = Mission.objects.filter(is_active=True)
        context['visions'] = Vision.objects.filter(is_active=True)
        context['values'] = Values.objects.filter(is_active=True)
        context['why_choose_us'] = WhyChooseUs.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(
            is_active=True, is_deleted=False, is_featured=True
        )[:6]
        context['featured_services'] = Service.objects.filter(
            is_active=True, is_deleted=False, is_featured=True
        )[:6]
        context['featured_projects'] = Project.objects.filter(
            is_active=True, is_deleted=False, is_featured=True
        )[:6]
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        context['clients'] = Client.objects.filter(is_active=True)
        context['latest_posts'] = BlogPost.objects.filter(
            is_published=True, is_deleted=False
        )[:3]
        context['seo'] = get_seo_context('/')
        return context


# -----------------------------------------------------------------------------
# About Page
# -----------------------------------------------------------------------------

class AboutView(TemplateView):
    template_name = 'website/pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.load()
        context['missions'] = Mission.objects.filter(is_active=True)
        context['visions'] = Vision.objects.filter(is_active=True)
        context['values'] = Values.objects.filter(is_active=True)
        context['why_choose_us'] = WhyChooseUs.objects.filter(is_active=True)
        context['seo'] = get_seo_context('/about/')
        return context


# -----------------------------------------------------------------------------
# Products
# -----------------------------------------------------------------------------

class ProductListView(ListView):
    model = Product
    template_name = 'website/pages/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True, is_deleted=False
        ).prefetch_related('features')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo'] = get_seo_context('/products/')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'website/pages/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.object.features.all()
        context['related_products'] = Product.objects.filter(
            is_active=True, is_deleted=False
        ).exclude(pk=self.object.pk)[:4]
        context['seo'] = get_seo_context(f'/products/{self.object.slug}/')
        return context


# -----------------------------------------------------------------------------
# Services
# -----------------------------------------------------------------------------

class ServiceListView(ListView):
    model = Service
    template_name = 'website/pages/services.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        return Service.objects.filter(
            is_active=True, is_deleted=False
        ).prefetch_related('features')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo'] = get_seo_context('/services/')
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'website/pages/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return Service.objects.filter(is_active=True, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.object.features.all()
        context['related_services'] = Service.objects.filter(
            is_active=True, is_deleted=False
        ).exclude(pk=self.object.pk)[:4]
        context['seo'] = get_seo_context(f'/services/{self.object.slug}/')
        return context


# -----------------------------------------------------------------------------
# Projects
# -----------------------------------------------------------------------------

class ProjectListView(ListView):
    model = Project
    template_name = 'website/pages/projects.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        queryset = Project.objects.filter(
            is_active=True, is_deleted=False
        ).prefetch_related('gallery_images', 'technologies')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Project.objects.filter(
            is_active=True, is_deleted=False
        ).exclude(category='').values_list('category', flat=True).distinct()
        context['seo'] = get_seo_context('/projects/')
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'website/pages/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(
            is_active=True, is_deleted=False
        ).prefetch_related('gallery_images', 'technologies')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.object.gallery_images.all()
        context['technologies'] = self.object.technologies.all()
        context['related_projects'] = Project.objects.filter(
            is_active=True, is_deleted=False, category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        context['seo'] = get_seo_context(f'/projects/{self.object.slug}/')
        return context


# -----------------------------------------------------------------------------
# Team
# -----------------------------------------------------------------------------

class TeamListView(ListView):
    model = TeamMember
    template_name = 'website/pages/team.html'
    context_object_name = 'members'

    def get_queryset(self):
        return TeamMember.objects.filter(
            is_active=True, is_deleted=False
        ).prefetch_related('skills')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['executives'] = self.get_queryset().filter(is_executive=True)[:3]
        context['seo'] = get_seo_context('/team/')
        return context


# -----------------------------------------------------------------------------
# Clients
# -----------------------------------------------------------------------------

class ClientListView(ListView):
    model = Client
    template_name = 'website/pages/clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
        context['seo'] = get_seo_context('/clients/')
        return context


# -----------------------------------------------------------------------------
# Careers
# -----------------------------------------------------------------------------

class CareerListView(ListView):
    model = JobOpening
    template_name = 'website/pages/careers.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return JobOpening.objects.filter(
            is_active=True, is_deleted=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['career_page'] = Career.load()
        context['seo'] = get_seo_context('/careers/')
        return context


class CareerDetailView(DetailView):
    model = JobOpening
    template_name = 'website/pages/career_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        return JobOpening.objects.filter(is_active=True, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo'] = get_seo_context(f'/careers/{self.object.slug}/')
        return context


# -----------------------------------------------------------------------------
# Blog
# -----------------------------------------------------------------------------

class BlogListView(ListView):
    model = BlogPost
    template_name = 'website/pages/blog.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.filter(
            is_published=True, is_deleted=False
        ).select_related('category').prefetch_related('tags')
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['featured_posts'] = BlogPost.objects.filter(
            is_published=True, is_deleted=False, is_featured=True
        )[:3]
        context['seo'] = get_seo_context('/blog/')
        return context


class BlogCategoryView(ListView):
    model = BlogPost
    template_name = 'website/pages/blog.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['slug'])
        return BlogPost.objects.filter(
            is_published=True, is_deleted=False, category=self.category
        ).prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = BlogCategory.objects.all()
        context['seo'] = get_seo_context(f'/blog/category/{self.category.slug}/')
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'website/pages/blog_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return BlogPost.objects.filter(
            is_published=True, is_deleted=False
        ).select_related('category').prefetch_related('tags')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = BlogPost.objects.filter(
            is_published=True, is_deleted=False
        ).exclude(pk=self.object.pk).select_related('category')[:3]
        context['seo'] = get_seo_context(f'/blog/{self.object.slug}/')
        return context


# -----------------------------------------------------------------------------
# Contact
# -----------------------------------------------------------------------------

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'website/pages/contact.html'
    success_url = '/contact/?submitted=1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInformation.objects.filter(is_active=True)
        context['social_links'] = SocialMedia.objects.filter(is_active=True)
        context['seo'] = get_seo_context('/contact/')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        message = form.save()
        self.send_contact_email(message)
        messages.success(
            self.request,
            'Thank you for contacting us. We will get back to you shortly.'
        )
        return response

    def send_contact_email(self, message):
        subject = f"Contact Form: {message.subject}"
        body = (
            f"Name: {message.name}\n"
            f"Email: {message.email}\n"
            f"Phone: {message.phone or 'N/A'}\n\n"
            f"Message:\n{message.message}"
        )
        recipient = getattr(settings, 'CONTACT_RECIPIENT_EMAIL', settings.DEFAULT_FROM_EMAIL)
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=True,
            )
        except Exception:
            pass


# -----------------------------------------------------------------------------
# Legal Pages
# -----------------------------------------------------------------------------

class PrivacyPolicyView(TemplateView):
    template_name = 'website/pages/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy'] = PrivacyPolicy.load()
        context['seo'] = get_seo_context('/privacy-policy/')
        return context


class TermsOfServiceView(TemplateView):
    template_name = 'website/pages/terms_of_service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = TermsOfService.load()
        context['seo'] = get_seo_context('/terms-of-service/')
        return context


# -----------------------------------------------------------------------------
# Newsletter
# -----------------------------------------------------------------------------

class NewsletterSubscribeView(View):
    """AJAX newsletter subscription endpoint."""

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Newsletter.objects.get_or_create(email=email, defaults={'is_active': True})
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing to our newsletter.'
            })
        return JsonResponse(
            {'success': False, 'message': 'Please enter a valid email address.'},
            status=400
        )
