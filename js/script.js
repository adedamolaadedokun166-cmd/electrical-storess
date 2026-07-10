// Loading screen
window.addEventListener('load', () => {
  const loader = document.querySelector('.loading-screen');
  if (loader) {
    loader.classList.add('hidden');
    setTimeout(() => loader.remove(), 400);
  }
});

function showToast(message) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(showToast.timeout);
  showToast.timeout = setTimeout(() => toast.classList.remove('show'), 2200);
}

// Scroll progress and sticky nav
const progressBar = document.querySelector('.scroll-progress');
const mainNav = document.getElementById('main-nav');
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  if (progressBar) progressBar.style.width = `${progress}%`;
  if (mainNav) mainNav.classList.toggle('scrolled', scrollTop > 40);
});

// Mobile navigation
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
if (menuToggle && navLinks) {
  menuToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navLinks.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Dark/light mode toggle
const themeToggle = document.querySelector('.theme-toggle');
const body = document.body;
const savedTheme = localStorage.getItem('theme');
if (savedTheme) body.setAttribute('data-theme', savedTheme);
if (themeToggle) {
  themeToggle.textContent = body.getAttribute('data-theme') === 'dark' ? '☀︎' : '☾';
  themeToggle.addEventListener('click', () => {
    const current = body.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    themeToggle.textContent = next === 'dark' ? '☀︎' : '☾';
    showToast(`Switched to ${next} mode`);
  });
}

// Scroll reveal
const revealItems = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });
revealItems.forEach((item) => revealObserver.observe(item));

// Animated counters
const counters = document.querySelectorAll('[data-count]');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const target = Number(el.getAttribute('data-count'));
      let count = 0;
      const step = Math.ceil(target / 60);
      const timer = setInterval(() => {
        count += step;
        if (count >= target) {
          el.textContent = target + '+';
          clearInterval(timer);
        } else {
          el.textContent = count;
        }
      }, 20);
      counterObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });
counters.forEach((counter) => counterObserver.observe(counter));

// Portfolio filter
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');
filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    filterButtons.forEach((btn) => btn.classList.remove('active'));
    button.classList.add('active');
    const filter = button.getAttribute('data-filter');
    projectCards.forEach((card) => {
      const matches = filter === 'all' || card.classList.contains(filter);
      card.classList.toggle('hidden', !matches);
    });
  });
});

// Product search and category filter
const searchInput = document.getElementById('product-search');
const categoryButtons = document.querySelectorAll('.chip');
const productCards = document.querySelectorAll('.product-card');
let activeCategory = 'all';

function filterProducts() {
  const query = searchInput?.value.toLowerCase() || '';
  productCards.forEach((card) => {
    const text = card.textContent.toLowerCase();
    const category = card.getAttribute('data-category') || '';
    const matchesCategory = activeCategory === 'all' || category === activeCategory;
    const matchesSearch = text.includes(query);
    card.style.display = matchesCategory && matchesSearch ? 'block' : 'none';
  });
}

searchInput?.addEventListener('input', filterProducts);
categoryButtons.forEach((button) => {
  button.addEventListener('click', () => {
    categoryButtons.forEach((chip) => chip.classList.remove('active'));
    button.classList.add('active');
    activeCategory = button.getAttribute('data-category') || 'all';
    filterProducts();
  });
});

// Testimonials slider
const testimonials = document.querySelectorAll('.testimonial-card');
const prevButton = document.querySelector('.slider-btn.prev');
const nextButton = document.querySelector('.slider-btn.next');
let testimonialIndex = 0;

function showTestimonial(index) {
  testimonials.forEach((card, cardIndex) => {
    card.classList.toggle('active', cardIndex === index);
  });
}

function nextTestimonial() {
  testimonialIndex = (testimonialIndex + 1) % testimonials.length;
  showTestimonial(testimonialIndex);
}

function prevTestimonial() {
  testimonialIndex = (testimonialIndex - 1 + testimonials.length) % testimonials.length;
  showTestimonial(testimonialIndex);
}

if (prevButton && nextButton && testimonials.length) {
  prevButton.addEventListener('click', prevTestimonial);
  nextButton.addEventListener('click', nextTestimonial);
  setInterval(nextTestimonial, 6000);
}

// FAQ accordion
const faqItems = document.querySelectorAll('.faq-item');
faqItems.forEach((item) => {
  item.querySelector('.faq-question').addEventListener('click', () => {
    const isActive = item.classList.contains('active');
    faqItems.forEach((faq) => faq.classList.remove('active'));
    if (!isActive) item.classList.add('active');
  });
});

// Back to top button
const backToTop = document.querySelector('.back-to-top');
window.addEventListener('scroll', () => {
  if (window.scrollY > 500) {
    backToTop.style.display = 'grid';
  } else {
    backToTop.style.display = 'none';
  }
});
backToTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Newsletter form mock submit
const newsletterForm = document.querySelector('.newsletter-form');
newsletterForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const input = newsletterForm.querySelector('input');
  if (input) {
    input.value = '';
    showToast('Thanks for subscribing!');
  }
});

// Cookie banner
const cookieBanner = document.getElementById('cookie-banner');
const cookieButtons = document.querySelectorAll('[data-cookie-choice]');
const cookiePreference = localStorage.getItem('cookieConsent');
if (!cookiePreference && cookieBanner) {
  cookieBanner.classList.add('show');
}
cookieButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const choice = button.getAttribute('data-cookie-choice');
    localStorage.setItem('cookieConsent', choice);
    cookieBanner?.classList.remove('show');
    showToast(choice === 'accept' ? 'Cookies enabled' : 'Cookies declined');
  });
});
