/*
 * Skyblue Technology — Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar-skyblue');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Newsletter AJAX subscription
    const newsletterForms = document.querySelectorAll('.newsletter-ajax-form');
    newsletterForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const messageEl = form.querySelector('.newsletter-message');
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.innerHTML : '';

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            }

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (messageEl) {
                    messageEl.textContent = data.message;
                    messageEl.className = 'newsletter-message mt-2 small ' + (data.success ? 'text-success' : 'text-danger');
                }
                if (data.success) {
                    form.reset();
                }
            })
            .catch(() => {
                if (messageEl) {
                    messageEl.textContent = 'Something went wrong. Please try again.';
                    messageEl.className = 'newsletter-message mt-2 small text-danger';
                }
            })
            .finally(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            });
        });
    });

    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 6000);
    });

    // Client logo infinite scroll (simple duplicate for marquee effect)
    const logoTrack = document.querySelector('.logo-track');
    if (logoTrack) {
        const items = logoTrack.innerHTML;
        logoTrack.innerHTML = items + items;
    }
});
