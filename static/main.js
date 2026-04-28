document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');
  const toggle = document.querySelector('.nav-toggle');
  const tocLinks = document.querySelectorAll('.sidebar-nav a');
  const headings = [];

  tocLinks.forEach(link => {
    const id = link.getAttribute('href')?.slice(1);
    if (id) {
      const el = document.getElementById(id);
      if (el) headings.push({ el, link });
    }
  });

  // Mobile nav toggle
  if (toggle) {
    toggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('open');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
    });
  }

  // Close mobile nav on link click
  tocLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      }
    });
  });

  // Scroll spy
  let ticking = false;
  function updateActive() {
    const scrollY = window.scrollY + 120;
    let current = null;
    for (const { el, link } of headings) {
      if (el.offsetTop <= scrollY) current = link;
    }
    tocLinks.forEach(l => l.classList.remove('active'));
    if (current) current.classList.add('active');
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateActive);
      ticking = true;
    }
  });

  updateActive();
});
