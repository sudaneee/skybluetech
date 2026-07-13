/*
 * Skyblue Technology — Django Admin Custom Scripts
 */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Add skyblue class to branding
        const branding = document.querySelector('#branding h1');
        if (branding) {
            const text = branding.innerHTML;
            branding.innerHTML = text.replace(
                'Skyblue',
                '<span class="site-name">Skyblue</span>'
            );
        }

        // Auto-collapse fieldsets that contain SEO
        const fieldsets = document.querySelectorAll('fieldset');
        fieldsets.forEach(function (fs) {
            const legend = fs.querySelector('h2, .fieldset-heading');
            if (legend && legend.textContent.toLowerCase().includes('seo')) {
                fs.classList.add('collapsed');
            }
        });

        // Confirm soft-delete actions
        const softDeleteActions = document.querySelectorAll(
            'select[name="action"] option[value="soft_delete_selected"]'
        );
        softDeleteActions.forEach(function (option) {
            option.textContent += ' (can be restored)';
        });
    });
})();
