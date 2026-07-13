# Skyblue Technology Corporate Website

A world-class, enterprise-grade corporate website for **Skyblue Technology**, built with Django. The website is fully database-driven, responsive, SEO-optimized, and production-ready.

---

## Features

- **Single Django App** (`website`) for all website logic
- **Database-driven content** — everything editable via Django Admin
- **Custom Django Admin** with Skyblue Technology branding and dashboard
- **Rich Text Editing** via CKEditor 5
- **SEO Ready** — meta tags, Open Graph, Twitter Cards, sitemap, robots.txt, Schema.org
- **Responsive Design** — works on desktop, tablet, and mobile
- **Modern UI** — Bootstrap 5, Bootstrap Icons, Google Fonts
- **Performance** — lazy loading, optimized static files with WhiteNoise
- **Security** — CSRF, XSS protection, SQL injection protection, secure forms
- **Future-ready** — PostgreSQL-compatible, easy to extend with REST API, portals, payments

---

## Technology Stack

- Python 3.12+
- Django 5.0+
- SQLite (development) / PostgreSQL-ready
- Bootstrap 5.3+
- Bootstrap Icons
- CKEditor 5
- WhiteNoise
- django-crispy-forms + crispy-bootstrap5
- django-widget-tweaks
- django-cleanup
- django-humanize

---

## Project Structure

```
SkyblueTechnology/
├── myenv/                  # Virtual environment
├── DjangoApp/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── website/                # Single app for all website logic
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── sitemaps.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   └── templatetags/
├── media/                  # User uploads
├── staticfiles/            # Collected static files
├── fixtures/               # Seed data scripts
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone / Open the Project

```bash
cd SkyBlueTech
```

### 2. Create Virtual Environment

```bash
python -m venv myenv
```

On Windows (Git Bash):
```bash
source myenv/Scripts/activate
```

On Linux/macOS:
```bash
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update values as needed:

```bash
cp .env.example .env
```

For production, set:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL` (PostgreSQL)
- Email settings

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Load Seed Data

```bash
python fixtures/seed_data.py
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Default Admin Credentials

If you loaded seed data and created the superuser via the automated setup:

- **Username:** `admin`
- **Password:** `admin12345`

> Change this password immediately after first login.

---

## Website Pages

- Home
- About Us
- Products
- Product Detail
- Services
- Service Detail
- Projects
- Project Detail
- Our Team
- Clients
- Careers
- Career Detail
- Blog
- Blog Detail
- Contact
- Privacy Policy
- Terms of Service
- 404 Page

---

## Admin Features

- Custom branded login page
- Dashboard with stat cards
- Image previews
- Rich text editing (CKEditor 5)
- Search, filters, pagination
- Bulk actions
- Collapsible sections
- Automatic slug generation
- Soft delete support

---

## SEO

- Dynamic meta title, description, keywords
- Open Graph and Twitter Cards
- Canonical URLs
- Schema.org JSON-LD
- `/sitemap.xml`
- `/robots.txt`

---

## Security

- CSRF protection on all forms
- XSS protection via template escaping
- SQL injection protection via Django ORM
- Secure media upload validation
- Environment-based secret key
- Security headers ready for production

---

## Performance

- Lazy loading images
- WhiteNoise for static file serving
- Optimized static file compression
- Efficient database queries with `select_related` / `prefetch_related`

---

## Future Scalability

The project is structured to easily support:

- PostgreSQL migration (set `DATABASE_URL`)
- Django REST Framework API
- SkyCollect Payment Gateway integration
- Customer Portal / School Portal / Hospital Portal / POS Portal
- Multi-tenancy
- Custom authentication system

---

## Support

For support or inquiries, contact **Skyblue Technology** at info@skybluetechnology.com.
