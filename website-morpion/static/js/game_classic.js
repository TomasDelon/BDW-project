/**
 * Gestion AJAX pour la partie classique : intercepte les formulaires
 * afin de rafraîchir uniquement la section du jeu et conserver le scroll.
 */
(function() {
  'use strict';

  const SECTION_SELECTOR = '.game-play-section';
  const DEFAULT_HASH = '#classic-game-play';

  let aiRefreshInFlight = false;
  let aiRefreshTimeoutId = null;

  function initClassicSection(root) {
    attachAjaxForms(root);
    attachAutoSubmitRadios(root);
    syncMorpionSelector(root);
    maybeAutoRefresh(root);
  }

  function syncMorpionSelector(root) {
    if (typeof window.initMorpionSelectorSync === 'function') {
      window.initMorpionSelectorSync(root);
    }
  }

  function maybeAutoRefresh(root) {
    const section = getSectionFromRoot(root);
    if (!section) {
      return;
    }
    if (section.dataset.aiJustPlayed !== 'true') {
      return;
    }
    if (aiRefreshInFlight) {
      return;
    }
    aiRefreshInFlight = true;
    if (aiRefreshTimeoutId) {
      clearTimeout(aiRefreshTimeoutId);
    }
    aiRefreshTimeoutId = window.setTimeout(function() {
      const promise = fetchAndSwap(window.location.pathname + window.location.search, {
        method: 'GET',
        headers: { 'X-Requested-With': 'fetch' },
        credentials: 'same-origin',
      });
      if (promise && typeof promise.finally === 'function') {
        promise.finally(function() {
          aiRefreshInFlight = false;
        });
      } else {
        aiRefreshInFlight = false;
      }
    }, 120);
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

  function submitAjaxForm(form, event) {
    event.preventDefault();
    const method = (form.method || 'GET').toUpperCase();
    const headers = { 'X-Requested-With': 'fetch' };
    let url = form.getAttribute('action') || (window.location.pathname + window.location.search);
    const hashIndex = url.indexOf('#');
    if (hashIndex !== -1) {
      url = url.slice(0, hashIndex);
    }

    const formData = new FormData(form);
    const submitter = event && event.submitter;
    if (submitter && submitter.name) {
      formData.append(submitter.name, submitter.value);
    }

    const options = {
      method,
      headers,
      credentials: 'same-origin',
    };

    if (method === 'GET') {
      const params = new URLSearchParams(formData);
      const baseUrl = url.split('?')[0];
      const query = params.toString();
      url = query ? `${baseUrl}?${query}` : baseUrl;
    } else {
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
      options.body = new URLSearchParams(formData).toString();
    }

    fetchAndSwap(url, options);
  }

  async function fetchAndSwap(url, options) {
    const currentSection = document.querySelector(SECTION_SELECTOR);
    if (!currentSection) {
      window.location.href = url;
      return;
    }

    const previousScroll = window.scrollY;
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
      initClassicSection(newSection);

      const finalUrl = response.url ? new URL(response.url) : new URL(url, window.location.origin);
      const hash = finalUrl.hash && finalUrl.hash.length > 0 ? finalUrl.hash : DEFAULT_HASH;
      window.history.replaceState({}, '', finalUrl.pathname + finalUrl.search + hash);

      requestAnimationFrame(function() {
        window.scrollTo({ top: previousScroll });
      });
    } catch (error) {
      console.error('Classic game AJAX failed:', error);
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
    initClassicSection(section);
  });

  function getSectionFromRoot(root) {
    if (!root) {
      return document.querySelector(SECTION_SELECTOR);
    }
    if (root.matches && root.matches(SECTION_SELECTOR)) {
      return root;
    }
    if (root.querySelector) {
      return root.querySelector(SECTION_SELECTOR);
    }
    return document.querySelector(SECTION_SELECTOR);
  }
})();
