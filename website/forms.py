"""
Forms for the Skyblue Technology website.
"""

from django import forms
from django.core.validators import EmailValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

from .models import ContactMessage, Newsletter


class ContactForm(forms.ModelForm):
    """Contact page form."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+234 000 000 0000',
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'How can we help?',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project...',
                'rows': 5,
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'contact-form'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='row g-3'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
                Column('subject', css_class='form-group col-md-6'),
                css_class='row g-3'
            ),
            Field('message', css_class='form-control mb-3'),
            Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg')
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required.')
        return email.lower()


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form."""

    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control',
                'aria-label': 'Email address'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('email'),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()
