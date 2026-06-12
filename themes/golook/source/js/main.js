/**
 * golook theme — main.js
 * Native JavaScript, no dependencies.
 */

document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  /* ===================================================================
   *  1. Dark Mode Toggle
   * =================================================================== */
  (function () {
    var html = document.documentElement;
    var toggleBtn = document.getElementById('theme-toggle');
    var STORAGE_KEY = 'theme';

    // --- Determine initial theme ---
    // Priority: localStorage > system preference > light (default)
    function getInitialTheme() {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored) return stored;
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
      return 'light';
    }

    // --- Apply theme ---
    function applyTheme(theme) {
      html.setAttribute('data-theme', theme);
      localStorage.setItem(STORAGE_KEY, theme);
      updateButtonIcon(theme);
    }

    // --- Update button icon ---
    function updateButtonIcon(theme) {
      if (!toggleBtn) return;
      var isDark = theme === 'dark';
      // Sun SVG (shown in dark mode — click to switch to light)
      // Moon SVG (shown in light mode — click to switch to dark)
      toggleBtn.innerHTML = isDark
        ? '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
        : '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
    }

    // --- Init ---
    applyTheme(getInitialTheme());

    // --- Listen for system preference changes ---
    var mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', function (e) {
        // Only auto-switch if user hasn't explicitly set a preference
        if (!localStorage.getItem(STORAGE_KEY)) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }

    // --- Toggle on click ---
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        var current = html.getAttribute('data-theme') || 'light';
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }
  })();

  /* ===================================================================
   *  2. Mobile Navigation Menu
   * =================================================================== */
  (function () {
    var hamburgerBtn = document.getElementById('nav-toggle');
    var navMenu = document.getElementById('nav-menu');
    var body = document.body;

    if (!hamburgerBtn || !navMenu) return;

    // Toggle menu on hamburger click
    hamburgerBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      body.classList.toggle('nav-open');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (e) {
      if (!body.classList.contains('nav-open')) return;
      if (!navMenu.contains(e.target) && !hamburgerBtn.contains(e.target)) {
        body.classList.remove('nav-open');
      }
    });

    // Close menu on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) {
        body.classList.remove('nav-open');
      }
    });
  })();

  /* ===================================================================
   *  3. Back to Top Button
   * =================================================================== */
  (function () {
    var backToTopBtn = document.getElementById('back-to-top');

    if (!backToTopBtn) return;

    // Show/hide on scroll
    var scrollHandler = function () {
      if (window.scrollY > 300) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    };

    // Throttled scroll listener for performance
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          scrollHandler();
          ticking = false;
        });
        ticking = true;
      }
    });

    // Smooth scroll to top
    backToTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  })();
});