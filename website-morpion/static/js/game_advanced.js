/**
 * Gestion AJAX pour la partie avancée : les formulaires et liens marqués se chargent
 * via fetch pour garder une expérience fluide sans rechargement complet.
 */
(function() {
  'use strict';

  const SECTION_SELECTOR = '.game-play-section';

  function initGameSection(root) {
    attachAjaxForms(root);
    attachAutoSubmitRadios(root);
    attachAjaxLinks(root);
  }

  function buildFragmentUrl(url) {
    try {
      const absolute = new URL(url, window.location.origin);
      if (
        absolute.pathname.startsWith('/partie-avancee') &&
        !absolute.pathname.startsWith('/partie-avancee-fragment')
      ) {
        absolute.pathname = absolute.pathname.replace('/partie-avancee', '/partie-avancee-fragment');
      }
      return absolute.pathname + absolute.search;
    } catch (e) {
      return url;
    }
  }

  function canonicalizeUrl(url) {
    try {
      const absolute = new URL(url, window.location.origin);
      if (absolute.pathname.startsWith('/partie-avancee-fragment')) {
        absolute.pathname = absolute.pathname.replace('/partie-avancee-fragment', '/partie-avancee');
      }
      return absolute.pathname + absolute.search;
    } catch (e) {
      return url;
    }
  }

  function attachAjaxForms(root) {
    const forms = root.querySelectorAll('form.ajax-form');
    forms.forEach(function(form) {
      if (form.dataset.ajaxBound === 'true') {
        return;
      }
      form.dataset.ajaxBound = 'true';
      form.addEventListener('submit', function(event) {
        submitAjaxForm(form, event);
      });
    });
  }

  function attachAutoSubmitRadios(root) {
    const radios = root.querySelectorAll('.auto-submit-radio');
    radios.forEach(function(radio) {
      if (radio.dataset.ajaxBound === 'true') {
        return;
      }
      radio.dataset.ajaxBound = 'true';
      radio.addEventListener('change', function(event) {
        const form = radio.form;
        if (form && form.classList.contains('ajax-form')) {
          submitAjaxForm(form, event);
        } else if (form && typeof form.submit === 'function') {
          form.submit();
        }
      });
    });
  }

  function attachAjaxLinks(root) {
    const links = root.querySelectorAll('a.ajax-link');
    links.forEach(function(link) {
      if (link.dataset.ajaxBound === 'true') {
        return;
      }
      link.dataset.ajaxBound = 'true';
      link.addEventListener('click', function(event) {
        event.preventDefault();
        const targetUrl = buildFragmentUrl(link.href);
        fetchAndSwap(targetUrl, { method: 'GET', headers: { 'X-Requested-With': 'fetch' } });
      });
    });
  }

  function submitAjaxForm(form, event) {
    event.preventDefault();
    const method = (form.method || 'GET').toUpperCase();
    const headers = { 'X-Requested-With': 'fetch' };
    let url = form.getAttribute('action') || window.location.pathname;
    const formData = new FormData(form);
    const submitter = event && event.submitter;
    if (submitter && submitter.name) {
      formData.append(submitter.name, submitter.value);
    }
    const options = { method, headers };

    if (method === 'GET') {
      const params = new URLSearchParams(formData);
      const baseUrl = url.split('?')[0];
      const query = params.toString();
      url = query ? `${baseUrl}?${query}` : baseUrl;
    } else {
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
      options.body = new URLSearchParams(formData).toString();
    }

    const targetUrl = buildFragmentUrl(url);
    fetchAndSwap(targetUrl, options);
  }

  async function fetchAndSwap(url, options) {
    const currentSection = document.querySelector(SECTION_SELECTOR);
    if (!currentSection) {
      window.location.href = url;
      return;
    }

    currentSection.classList.add('is-loading');

    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const text = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(text, 'text/html');
      const newSection = doc.querySelector(SECTION_SELECTOR);

      if (!newSection) {
        window.location.href = url;
        return;
      }

      currentSection.replaceWith(newSection);
      initGameSection(newSection);

      const finalUrl = response.url ? new URL(response.url) : new URL(url, window.location.origin);
      const relativeUrl = canonicalizeUrl(finalUrl.href);
      window.history.replaceState({}, '', relativeUrl);
    } catch (error) {
      console.error('AJAX update failed:', error);
      window.location.href = url;
    } finally {
      const section = document.querySelector(SECTION_SELECTOR);
      if (section) {
        section.classList.remove('is-loading');
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    const section = document.querySelector(SECTION_SELECTOR) || document;
    initGameSection(section);
  });
})();
