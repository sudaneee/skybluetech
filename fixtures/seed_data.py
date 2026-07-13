"""
Seed data script for Skyblue Technology.

Run with:
    python manage.py shell < fixtures/seed_data.py

This creates all initial content required for the website to look complete.
"""

import os
import sys
import django

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')
django.setup()

from website.models import (
    SiteSettings, SiteSEO, HeroSection, About, Mission, Vision, Values,
    WhyChooseUs, Product, ProductFeature, Service, ServiceFeature,
    Project, ProjectImage, ProjectTechnology, TeamMember, TeamSkill,
    Client, Testimonial, BlogCategory, BlogTag, BlogPost, Gallery,
    ContactInformation, SocialMedia, FAQs, Career, JobOpening,
    PrivacyPolicy, TermsOfService
)


def create_singletons():
    """Create singleton models."""
    SiteSettings.objects.get_or_create(pk=1, defaults={
        'site_name': 'Skyblue Technology',
        'tagline': 'Innovative Technology Solutions for a Smarter Tomorrow',
        'footer_text': 'Delivering world-class technology solutions across education, healthcare, commerce, and financial services.',
        'copyright_text': '© Skyblue Technology. All rights reserved.',
        'contact_email': 'info@skybluetechnology.com',
        'contact_phone': '+234 000 000 0000',
        'address': 'Skyblue Technology Headquarters, Nigeria',
        'working_hours': 'Monday - Friday: 9:00 AM - 5:00 PM',
    })

    About.objects.get_or_create(pk=1, defaults={
        'title': 'About Skyblue Technology',
        'content': '<p>Skyblue Technology is a leading technology company dedicated to delivering innovative software solutions that transform businesses and institutions. With years of experience and a passionate team, we provide tailored technology products and services across education, healthcare, commerce, and financial technology.</p>',
        'years_experience': 10,
        'clients_served': 500,
        'projects_completed': 1200,
        'countries_served': 5,
    })

    Career.objects.get_or_create(pk=1, defaults={
        'title': 'Careers at Skyblue Technology',
        'content': '<p>Join our team of innovators, creators, and problem-solvers. At Skyblue Technology, we believe in nurturing talent and providing an environment where everyone can thrive.</p>',
    })

    PrivacyPolicy.objects.get_or_create(pk=1, defaults={
        'title': 'Privacy Policy',
        'content': '<p>Your privacy is important to us. This policy explains how we collect, use, and protect your personal information.</p><h3>Information We Collect</h3><p>We collect information you provide directly to us, such as when you fill out a contact form or subscribe to our newsletter.</p><h3>How We Use Information</h3><p>We use the information to respond to inquiries, improve our services, and send updates.</p><h3>Security</h3><p>We implement appropriate security measures to protect your data.</p>',
    })

    TermsOfService.objects.get_or_create(pk=1, defaults={
        'title': 'Terms of Service',
        'content': '<p>These terms govern your use of our website and services.</p><h3>Acceptance of Terms</h3><p>By accessing our website, you agree to these terms.</p><h3>Use of Services</h3><p>You agree to use our services lawfully and responsibly.</p><h3>Limitation of Liability</h3><p>Skyblue Technology is not liable for indirect damages arising from the use of our services.</p>',
    })


def create_seo():
    """Create default SEO entries."""
    seo_data = [
        {'page_path': '/', 'meta_title': 'Home', 'meta_description': 'Skyblue Technology - Innovative technology solutions for education, healthcare, commerce, and payments.', 'keywords': 'technology, software, solutions, skyblue'},
        {'page_path': '/about/', 'meta_title': 'About Us', 'meta_description': 'Learn about Skyblue Technology, our mission, vision, and values.', 'keywords': 'about, company, mission, vision'},
        {'page_path': '/products/', 'meta_title': 'Our Products', 'meta_description': 'Explore Skyblue Technology products including School Management, Hospital Management, POS, and SkyCollect.', 'keywords': 'products, school software, hospital software, pos, skycollect'},
        {'page_path': '/services/', 'meta_title': 'Our Services', 'meta_description': 'Comprehensive technology services from Skyblue Technology.', 'keywords': 'services, software development, web development, cloud, cybersecurity'},
        {'page_path': '/projects/', 'meta_title': 'Our Projects', 'meta_description': 'View our portfolio of completed technology projects.', 'keywords': 'projects, portfolio, case studies'},
        {'page_path': '/team/', 'meta_title': 'Our Team', 'meta_description': 'Meet the leadership and team behind Skyblue Technology.', 'keywords': 'team, executives, leadership'},
        {'page_path': '/clients/', 'meta_title': 'Our Clients', 'meta_description': 'Organizations that trust Skyblue Technology.', 'keywords': 'clients, testimonials'},
        {'page_path': '/careers/', 'meta_title': 'Careers', 'meta_description': 'Join the Skyblue Technology team.', 'keywords': 'careers, jobs, vacancies'},
        {'page_path': '/blog/', 'meta_title': 'Blog', 'meta_description': 'Latest news and insights from Skyblue Technology.', 'keywords': 'blog, news, insights, technology'},
        {'page_path': '/contact/', 'meta_title': 'Contact Us', 'meta_description': 'Get in touch with Skyblue Technology.', 'keywords': 'contact, support, inquiry'},
        {'page_path': '/privacy-policy/', 'meta_title': 'Privacy Policy', 'meta_description': 'Skyblue Technology privacy policy.', 'keywords': 'privacy policy'},
        {'page_path': '/terms-of-service/', 'meta_title': 'Terms of Service', 'meta_description': 'Skyblue Technology terms of service.', 'keywords': 'terms of service'},
    ]
    for data in seo_data:
        SiteSEO.objects.get_or_create(page_path=data['page_path'], defaults=data)


def create_contact_and_social():
    """Create contact info and social media links."""
    contact_data = [
        {'type': 'address', 'label': 'Head Office', 'value': 'Skyblue Technology Headquarters\nNigeria', 'icon': 'bi-geo-alt', 'is_primary': True, 'order': 1},
        {'type': 'phone', 'label': 'Phone', 'value': '+234 000 000 0000', 'icon': 'bi-telephone', 'is_primary': True, 'order': 2},
        {'type': 'email', 'label': 'Email', 'value': 'info@skybluetechnology.com', 'icon': 'bi-envelope', 'is_primary': True, 'order': 3},
        {'type': 'working_hours', 'label': 'Working Hours', 'value': 'Monday - Friday: 9:00 AM - 5:00 PM', 'icon': 'bi-clock', 'is_primary': False, 'order': 4},
    ]
    for data in contact_data:
        ContactInformation.objects.get_or_create(label=data['label'], defaults=data)

    social_data = [
        {'platform': 'facebook', 'url': 'https://facebook.com/skybluetechnology', 'order': 1},
        {'platform': 'twitter', 'url': 'https://twitter.com/skybluetech', 'order': 2},
        {'platform': 'linkedin', 'url': 'https://linkedin.com/company/skybluetechnology', 'order': 3},
        {'platform': 'instagram', 'url': 'https://instagram.com/skybluetechnology', 'order': 4},
    ]
    for data in social_data:
        SocialMedia.objects.get_or_create(platform=data['platform'], defaults=data)


def create_hero():
    """Create hero slide."""
    HeroSection.objects.get_or_create(headline='Innovative Technology Solutions', defaults={
        'subheadline': 'Empowering education, healthcare, commerce, and financial services with world-class software solutions.',
        'cta_text': 'Get Started',
        'cta_url': '/contact/',
        'secondary_cta_text': 'Explore Products',
        'secondary_cta_url': '/products/',
        'is_active': True,
        'order': 1,
    })


def create_mission_vision_values():
    """Create mission, vision, values, and why choose us."""
    missions = [
        {'title': 'Empowering Organizations', 'description': 'We build technology that empowers schools, hospitals, and businesses to operate more efficiently.', 'icon': 'bi-bullseye'},
        {'title': 'Simplifying Complexity', 'description': 'We transform complex processes into simple, intuitive digital experiences.', 'icon': 'bi-magic'},
    ]
    for i, data in enumerate(missions, 1):
        Mission.objects.get_or_create(title=data['title'], defaults={**data, 'order': i})

    visions = [
        {'title': 'A Digitally Transformed Africa', 'description': 'To be the leading technology partner driving digital transformation across Africa.', 'icon': 'bi-eye'},
        {'title': 'Innovation for Everyone', 'description': 'To make powerful technology accessible to every organization, regardless of size.', 'icon': 'bi-lightbulb'},
    ]
    for i, data in enumerate(visions, 1):
        Vision.objects.get_or_create(title=data['title'], defaults={**data, 'order': i})

    values = [
        {'title': 'Innovation', 'description': 'We constantly explore new ideas and technologies to deliver cutting-edge solutions.', 'icon': 'bi-lightbulb'},
        {'title': 'Integrity', 'description': 'We operate with honesty, transparency, and accountability in all our dealings.', 'icon': 'bi-shield-check'},
        {'title': 'Excellence', 'description': 'We are committed to delivering the highest quality in every project we undertake.', 'icon': 'bi-award'},
        {'title': 'Customer Focus', 'description': 'We put our clients at the center of everything we do.', 'icon': 'bi-people'},
    ]
    for i, data in enumerate(values, 1):
        Values.objects.get_or_create(title=data['title'], defaults={**data, 'order': i})

    reasons = [
        {'title': 'Innovation', 'description': 'We leverage the latest technologies to build future-ready solutions.', 'icon': 'bi-lightbulb'},
        {'title': 'Professionalism', 'description': 'Our team delivers with discipline, expertise, and attention to detail.', 'icon': 'bi-briefcase'},
        {'title': 'Customer Satisfaction', 'description': 'We prioritize client success and long-term partnerships.', 'icon': 'bi-heart'},
        {'title': 'Experienced Team', 'description': 'Years of experience across diverse industries and technology stacks.', 'icon': 'bi-people'},
        {'title': 'Support', 'description': 'Reliable support to keep your systems running smoothly.', 'icon': 'bi-headset'},
        {'title': 'Security', 'description': 'Robust security practices to protect your data and operations.', 'icon': 'bi-shield-lock'},
        {'title': 'Scalability', 'description': 'Solutions designed to grow with your organization.', 'icon': 'bi-graph-up-arrow'},
    ]
    for i, data in enumerate(reasons, 1):
        WhyChooseUs.objects.get_or_create(title=data['title'], defaults={**data, 'order': i})


def create_products():
    """Create products with features."""
    products = [
        {
            'title': 'School Management System',
            'slug': 'school-management-system',
            'short_description': 'A complete solution for managing admissions, records, exams, finance, and communication in schools.',
            'description': '<p>Our School Management System streamlines every aspect of school administration, from admissions to graduation. It includes modules for student records, result management, CBT, attendance, finance, parent and staff portals, library, hostel, timetable, examinations, and SMS notifications.</p><p>With integrated SkyCollect, fee collection becomes seamless and transparent.</p>',
            'icon': 'bi-mortarboard',
            'is_featured': True,
            'order': 1,
            'features': [
                'Admissions', 'Student Records', 'Result Management', 'CBT',
                'Attendance', 'Finance', 'Parent Portal', 'Staff Portal',
                'Library', 'Hostel', 'Timetable', 'Examinations',
                'SMS Notifications', 'Integrated SkyCollect'
            ],
        },
        {
            'title': 'Hospital Management System',
            'slug': 'hospital-management-system',
            'short_description': 'Comprehensive healthcare management software for hospitals and clinics.',
            'description': '<p>Our Hospital Management System digitizes patient records, appointments, laboratory, radiology, billing, pharmacy, and reporting. It helps healthcare providers deliver better care while improving operational efficiency.</p><p>Integrated SkyCollect ensures smooth payment processing for patients and hospitals.</p>',
            'icon': 'bi-hospital',
            'is_featured': True,
            'order': 2,
            'features': [
                'Patient Records', 'Doctors', 'Appointments', 'Laboratory',
                'Radiology', 'Billing', 'Pharmacy', 'Reports',
                'Integrated SkyCollect'
            ],
        },
        {
            'title': 'Point of Sale Management System',
            'slug': 'point-of-sale-management-system',
            'short_description': 'A powerful POS system with inventory, barcode, sales, and analytics.',
            'description': '<p>Our POS Management System helps retailers manage inventory, barcode scanning, sales, reports, customers, suppliers, expenses, receipts, and analytics from a single platform.</p><p>SkyCollect integration enables fast and secure payment collections.</p>',
            'icon': 'bi-cart4',
            'is_featured': True,
            'order': 3,
            'features': [
                'Inventory', 'Barcode', 'Sales', 'Reports',
                'Customers', 'Suppliers', 'Expenses', 'Receipts',
                'Analytics', 'Integrated SkyCollect'
            ],
        },
        {
            'title': 'SkyCollect',
            'slug': 'skycollect',
            'short_description': 'A standalone flagship payment and collection platform powering all our solutions.',
            'description': '<p>SkyCollect is our flagship financial technology product. It powers payment collections across every Skyblue Technology solution and beyond. Features include wallet management, virtual accounts, payment gateway, school payments, hospital payments, merchant payments, settlement, analytics, transaction monitoring, and enterprise-grade security.</p>',
            'icon': 'bi-cloud-check-fill',
            'is_featured': True,
            'order': 4,
            'features': [
                'Wallet', 'Virtual Accounts', 'Payment Gateway', 'School Payments',
                'Hospital Payments', 'Merchant Payments', 'Settlement',
                'Analytics', 'Transaction Monitoring', 'Security'
            ],
        },
    ]

    for product_data in products:
        features = product_data.pop('features')
        product, created = Product.objects.get_or_create(slug=product_data['slug'], defaults=product_data)
        if created:
            for i, feature_name in enumerate(features, 1):
                ProductFeature.objects.create(product=product, name=feature_name, order=i)


def create_services():
    """Create services."""
    services = [
        {
            'title': 'Software Development',
            'slug': 'software-development',
            'short_description': 'Custom software solutions tailored to your business needs.',
            'description': '<p>We design and develop custom software applications that solve real business problems. From desktop to mobile and web applications, our team delivers scalable and maintainable solutions.</p>',
            'icon': 'bi-code-slash',
            'is_featured': True,
            'order': 1,
        },
        {
            'title': 'Web Development',
            'slug': 'web-development',
            'short_description': 'Modern, responsive, and high-performance websites.',
            'description': '<p>We build professional websites and web applications using the latest technologies. Our designs are responsive, SEO-friendly, and optimized for performance.</p>',
            'icon': 'bi-globe',
            'is_featured': True,
            'order': 2,
        },
        {
            'title': 'Website Hosting',
            'slug': 'website-hosting',
            'short_description': 'Reliable and secure hosting for your web applications.',
            'description': '<p>Our hosting services ensure your website is always available, secure, and fast. We offer shared, VPS, and dedicated hosting options.</p>',
            'icon': 'bi-server',
            'is_featured': True,
            'order': 3,
        },
        {
            'title': 'Email Hosting',
            'slug': 'email-hosting',
            'short_description': 'Professional business email hosting solutions.',
            'description': '<p>Get professional email addresses for your business with our secure and reliable email hosting services.</p>',
            'icon': 'bi-envelope-at',
            'is_featured': False,
            'order': 4,
        },
        {
            'title': 'Cloud Services',
            'slug': 'cloud-services',
            'short_description': 'Cloud migration, management, and consulting.',
            'description': '<p>We help businesses leverage the power of cloud computing through migration, management, and optimization services.</p>',
            'icon': 'bi-cloud-arrow-up',
            'is_featured': True,
            'order': 5,
        },
        {
            'title': 'ICT Consultancy',
            'slug': 'ict-consultancy',
            'short_description': 'Expert guidance for your technology strategy.',
            'description': '<p>Our consultants provide strategic ICT advice to help organizations make informed technology decisions and achieve digital transformation.</p>',
            'icon': 'bi-chat-square-text',
            'is_featured': False,
            'order': 6,
        },
        {
            'title': 'Networking',
            'slug': 'networking',
            'short_description': 'Design, installation, and management of network infrastructure.',
            'description': '<p>We design and implement reliable network infrastructure for businesses, schools, and healthcare facilities.</p>',
            'icon': 'bi-diagram-3',
            'is_featured': False,
            'order': 7,
        },
        {
            'title': 'Cybersecurity',
            'slug': 'cybersecurity',
            'short_description': 'Protect your business from cyber threats.',
            'description': '<p>Our cybersecurity services include risk assessment, vulnerability management, security audits, and implementation of protective measures.</p>',
            'icon': 'bi-shield-lock',
            'is_featured': True,
            'order': 8,
        },
        {
            'title': 'IT Training',
            'slug': 'it-training',
            'short_description': 'Professional training to upskill your team.',
            'description': '<p>We offer practical IT training programs for individuals and organizations, covering software development, networking, cybersecurity, and more.</p>',
            'icon': 'bi-mortarboard',
            'is_featured': False,
            'order': 9,
        },
        {
            'title': 'Managed Services',
            'slug': 'managed-services',
            'short_description': 'End-to-end IT management and support.',
            'description': '<p>Focus on your core business while we manage your IT infrastructure, support, and maintenance needs.</p>',
            'icon': 'bi-headset',
            'is_featured': False,
            'order': 10,
        },
    ]

    for service_data in services:
        Service.objects.get_or_create(slug=service_data['slug'], defaults=service_data)


def create_team():
    """Create the three executives."""
    team = [
        {
            'name': 'Engr. Usman Ibrahim',
            'role': 'Founder & CEO',
            'biography': '<p>Engr. Usman Ibrahim is the visionary Founder and CEO of Skyblue Technology. With a strong engineering background and a passion for technology, he leads the company in delivering transformative solutions across multiple sectors.</p>',
            'email': 'usman.ibrahim@skybluetechnology.com',
            'phone': '+234 000 000 0001',
            'linkedin': 'https://linkedin.com/in/usmanibrahim',
            'facebook': 'https://facebook.com/usmanibrahim',
            'is_executive': True,
            'order': 1,
            'skills': [('Leadership', 98), ('Strategy', 95), ('Engineering', 92)],
        },
        {
            'name': 'Ismail Abbas',
            'role': 'Technical Partner',
            'biography': '<p>Ismail Abbas is the Technical Partner at Skyblue Technology. He oversees the technical direction of the company, ensuring that products are built with modern, scalable, and secure technologies.</p>',
            'email': 'ismail.abbas@skybluetechnology.com',
            'linkedin': 'https://linkedin.com/in/ismailabbas',
            'twitter': 'https://twitter.com/ismailabbas',
            'is_executive': True,
            'order': 2,
            'skills': [('Software Architecture', 96), ('Django/Python', 95), ('Cloud Computing', 90)],
        },
        {
            'name': 'Yusuf Musa',
            'role': 'Business Intelligence Partner',
            'biography': '<p>Yusuf Musa is the Business Intelligence Partner at Skyblue Technology. He leverages data and analytics to drive business decisions and help clients optimize their operations.</p>',
            'email': 'yusuf.musa@skybluetechnology.com',
            'linkedin': 'https://linkedin.com/in/yusufmusa',
            'facebook': 'https://facebook.com/yusufmusa',
            'is_executive': True,
            'order': 3,
            'skills': [('Data Analytics', 94), ('Business Strategy', 92), ('Reporting', 90)],
        },
    ]

    for member_data in team:
        skills = member_data.pop('skills')
        member, created = TeamMember.objects.get_or_create(name=member_data['name'], defaults=member_data)
        if created:
            for skill_name, proficiency in skills:
                TeamSkill.objects.create(member=member, name=skill_name, proficiency=proficiency)


def create_projects():
    """Create sample projects."""
    projects = [
        {
            'title': 'Digital Transformation for Metropolitan School',
            'slug': 'metropolitan-school-digital',
            'client': 'Metropolitan School',
            'category': 'Education',
            'description': '<p>We implemented our School Management System for Metropolitan School, digitizing admissions, attendance, examinations, finance, and parent communication. The project resulted in improved efficiency and parent satisfaction.</p>',
            'status': 'completed',
            'is_featured': True,
            'order': 1,
            'technologies': ['Django', 'PostgreSQL', 'Bootstrap', 'CKEditor'],
        },
        {
            'title': 'Hospital Management System for CityCare Clinic',
            'slug': 'citycare-hospital-system',
            'client': 'CityCare Clinic',
            'category': 'Healthcare',
            'description': '<p>CityCare Clinic partnered with us to deploy a comprehensive Hospital Management System. The solution covers patient records, appointments, billing, laboratory, and pharmacy operations.</p>',
            'status': 'completed',
            'is_featured': True,
            'order': 2,
            'technologies': ['Django', 'SQLite', 'WhiteNoise', 'Pillow'],
        },
        {
            'title': 'POS & Payment Integration for QuickMart',
            'slug': 'quickmart-pos-integration',
            'client': 'QuickMart Retail',
            'category': 'Retail',
            'description': '<p>We deployed our Point of Sale Management System integrated with SkyCollect for QuickMart Retail. The solution streamlines inventory, sales, receipts, and payment collections.</p>',
            'status': 'completed',
            'is_featured': True,
            'order': 3,
            'technologies': ['Django', 'SkyCollect API', 'Bootstrap', 'Chart.js'],
        },
    ]

    for project_data in projects:
        technologies = project_data.pop('technologies')
        project, created = Project.objects.get_or_create(slug=project_data['slug'], defaults=project_data)
        if created:
            for tech_name in technologies:
                ProjectTechnology.objects.create(project=project, name=tech_name)


def create_clients_and_testimonials():
    """Create clients and testimonials."""
    clients = [
        {'name': 'Metropolitan School', 'website': 'https://example.com/metropolitan'},
        {'name': 'CityCare Clinic', 'website': 'https://example.com/citycare'},
        {'name': 'QuickMart Retail', 'website': 'https://example.com/quickmart'},
        {'name': 'Alpha Logistics', 'website': 'https://example.com/alpha'},
        {'name': 'Nova Healthcare', 'website': 'https://example.com/nova'},
    ]
    created_clients = []
    for data in clients:
        client, _ = Client.objects.get_or_create(name=data['name'], defaults={**data, 'is_active': True})
        created_clients.append(client)

    testimonials = [
        {
            'client': created_clients[0],
            'author_name': 'Dr. Amina Bello',
            'author_title': 'Principal',
            'company': 'Metropolitan School',
            'comment': 'Skyblue Technology transformed how we manage our school. The School Management System is intuitive, reliable, and has greatly improved communication with parents.',
            'rating': 5,
        },
        {
            'client': created_clients[1],
            'author_name': 'Dr. James Okonkwo',
            'author_title': 'Medical Director',
            'company': 'CityCare Clinic',
            'comment': 'The Hospital Management System has streamlined our operations. Patient records, billing, and appointments are now seamlessly managed in one platform.',
            'rating': 5,
        },
        {
            'client': created_clients[2],
            'author_name': 'Fatima Abdullahi',
            'author_title': 'Operations Manager',
            'company': 'QuickMart Retail',
            'comment': 'Integrating SkyCollect with our POS system has made payment collection faster and more secure. Excellent service and support from the Skyblue team.',
            'rating': 5,
        },
    ]
    for data in testimonials:
        Testimonial.objects.get_or_create(author_name=data['author_name'], defaults={**data, 'is_active': True})


def create_blog():
    """Create blog categories, tags, and posts."""
    categories = [
        {'name': 'Technology', 'slug': 'technology'},
        {'name': 'Company News', 'slug': 'company-news'},
        {'name': 'Industry Insights', 'slug': 'industry-insights'},
    ]
    created_categories = {}
    for data in categories:
        cat, _ = BlogCategory.objects.get_or_create(slug=data['slug'], defaults=data)
        created_categories[data['slug']] = cat

    tags = [
        {'name': 'SkyCollect', 'slug': 'skycollect'},
        {'name': 'Education', 'slug': 'education'},
        {'name': 'Healthcare', 'slug': 'healthcare'},
    ]
    created_tags = {}
    for data in tags:
        tag, _ = BlogTag.objects.get_or_create(slug=data['slug'], defaults=data)
        created_tags[data['slug']] = tag

    posts = [
        {
            'title': 'How SkyCollect is Revolutionizing Payments',
            'slug': 'skycollect-revolutionizing-payments',
            'category': created_categories['technology'],
            'excerpt': 'Discover how SkyCollect simplifies payment collection across schools, hospitals, and merchants.',
            'content': '<p>Payment collection has always been a challenge for institutions and businesses. SkyCollect changes the game by providing a unified platform for wallet management, virtual accounts, payment gateway integration, and real-time transaction monitoring.</p><p>Whether you are a school collecting fees, a hospital processing patient payments, or a merchant receiving payments, SkyCollect ensures fast, secure, and transparent transactions.</p>',
            'is_featured': True,
            'is_published': True,
            'tags': [created_tags['skycollect']],
        },
        {
            'title': 'The Future of Education Technology',
            'slug': 'future-of-education-technology',
            'category': created_categories['industry-insights'],
            'excerpt': 'Explore the trends shaping the future of education technology in Africa.',
            'content': '<p>Education technology is evolving rapidly. From digital classrooms to AI-powered learning management systems, schools are embracing technology to improve learning outcomes and administrative efficiency.</p><p>Skyblue Technology is at the forefront of this transformation with our comprehensive School Management System.</p>',
            'is_featured': False,
            'is_published': True,
            'tags': [created_tags['education']],
        },
        {
            'title': 'Welcome to the New Skyblue Technology Website',
            'slug': 'welcome-new-website',
            'category': created_categories['company-news'],
            'excerpt': 'We are excited to launch our new corporate website. Learn more about our products and services.',
            'content': '<p>We are thrilled to announce the launch of our new corporate website. The website showcases our products, services, projects, and team, and is fully managed through our admin dashboard.</p><p>Stay tuned for more updates and insights from Skyblue Technology.</p>',
            'is_featured': True,
            'is_published': True,
            'tags': [],
        },
    ]

    for post_data in posts:
        tags = post_data.pop('tags')
        post, created = BlogPost.objects.get_or_create(slug=post_data['slug'], defaults=post_data)
        if created:
            post.tags.set(tags)


def create_faqs_and_jobs():
    """Create FAQs and job openings."""
    faqs = [
        {'question': 'What services does Skyblue Technology offer?', 'answer': '<p>We offer software development, web development, hosting, cloud services, ICT consultancy, networking, cybersecurity, IT training, and managed services.</p>'},
        {'question': 'What products does Skyblue Technology provide?', 'answer': '<p>Our products include School Management System, Hospital Management System, Point of Sale Management System, and SkyCollect.</p>'},
        {'question': 'How can I contact Skyblue Technology?', 'answer': '<p>You can reach us through the contact form on our website, by email, or by phone.</p>'},
        {'question': 'Is SkyCollect secure?', 'answer': '<p>Yes, SkyCollect is built with enterprise-grade security to protect all transactions and user data.</p>'},
    ]
    for i, data in enumerate(faqs, 1):
        FAQs.objects.get_or_create(question=data['question'], defaults={**data, 'order': i, 'is_active': True})

    jobs = [
        {
            'title': 'Senior Software Engineer',
            'slug': 'senior-software-engineer',
            'department': 'Engineering',
            'location': 'Abuja, Nigeria',
            'type': 'full_time',
            'description': '<p>We are looking for an experienced Software Engineer to join our team and lead the development of innovative products.</p>',
            'requirements': '<ul><li>Bachelor\'s degree in Computer Science or related field</li><li>5+ years of software development experience</li><li>Proficiency in Python and Django</li><li>Experience with cloud platforms</li></ul>',
            'benefits': '<ul><li>Competitive salary</li><li>Health insurance</li><li>Professional development</li></ul>',
        },
        {
            'title': 'Business Development Manager',
            'slug': 'business-development-manager',
            'department': 'Sales',
            'location': 'Lagos, Nigeria',
            'type': 'full_time',
            'description': '<p>We are seeking a Business Development Manager to drive growth and build strong client relationships.</p>',
            'requirements': '<ul><li>Bachelor\'s degree in Business or related field</li><li>3+ years of sales experience in technology</li><li>Strong communication and negotiation skills</li></ul>',
        },
    ]
    for job_data in jobs:
        JobOpening.objects.get_or_create(slug=job_data['slug'], defaults={**job_data, 'is_active': True})


if __name__ == '__main__':
    create_singletons()
    create_seo()
    create_contact_and_social()
    create_hero()
    create_mission_vision_values()
    create_products()
    create_services()
    create_team()
    create_projects()
    create_clients_and_testimonials()
    create_blog()
    create_faqs_and_jobs()
    print('Seed data created successfully.')
