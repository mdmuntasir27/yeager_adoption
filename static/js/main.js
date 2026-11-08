// Theme management
(function () {
    const THEME_KEY = 'yeager-theme';

    function getStoredTheme() {
        return localStorage.getItem(THEME_KEY);
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        updateToggleIcon(theme);
    }

    function updateToggleIcon(theme) {
        const btn = document.getElementById('theme-toggle');
        if (btn) {
            btn.textContent = theme === 'dark' ? '☀' : '☾';
            btn.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
        }
    }

    function initTheme() {
        const stored = getStoredTheme();
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = stored || (prefersDark ? 'dark' : 'light');
        setTheme(theme);
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
    }

    // Apply theme immediately to avoid flash
    initTheme();

    document.addEventListener('DOMContentLoaded', function () {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            const current = document.documentElement.getAttribute('data-theme');
            updateToggleIcon(current);
            toggleBtn.addEventListener('click', toggleTheme);
        }

        // Mobile nav hamburger
        const hamburger = document.getElementById('nav-hamburger');
        const navLinks = document.getElementById('nav-links');
        if (hamburger && navLinks) {
            hamburger.addEventListener('click', function () {
                navLinks.classList.toggle('open');
            });
        }
    });
})();

// Favorite toggle
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.favorite-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const petId = btn.dataset.petId;
            const csrfToken = getCookie('csrftoken');

            fetch('/pets/' + petId + '/favorite/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(function (resp) { return resp.json(); })
            .then(function (data) {
                if (data.status === 'added') {
                    btn.classList.add('active');
                    btn.querySelector('.fav-text').textContent = 'Unfavorite';
                } else {
                    btn.classList.remove('active');
                    btn.querySelector('.fav-text').textContent = 'Favorite';
                }
            })
            .catch(function (err) {
                console.error('Favorite toggle failed', err);
            });
        });
    });
});

function getCookie(name) {
    let value = '; ' + document.cookie;
    let parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 500);
        }, 4000);
    });
});

