/**
 * main.js — CE Python Portal
 * TOC highlighting, copy code, reading progress, mobile sidebar
 */

/* ── Copy code ────────────────────────────────────────────────────────── */
function copyCode(btn) {
  // Find the code element inside the same article
  const article = btn.closest('.nb-cell');
  const pre = article.querySelector('.hl pre');
  if (!pre) return;
  const text = pre.innerText;
  navigator.clipboard.writeText(text).then(() => {
    btn.classList.add('copied');
    const original = btn.innerHTML;
    btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
      <polyline points="20 6 9 17 4 12"/></svg> ¡Copiado!`;
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.innerHTML = original;
    }, 2000);
  }).catch(() => {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  });
}

/* ── Reading progress bar ─────────────────────────────────────────────── */
const progressBar = document.getElementById('readProgress');
if (progressBar) {
  window.addEventListener('scroll', () => {
    const main = document.getElementById('nbMain') || document.body;
    const scrollTop = window.scrollY;
    const docHeight = main.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? Math.min((scrollTop / docHeight) * 100, 100) : 0;
    progressBar.style.width = pct + '%';
  }, { passive: true });
}

/* ── Active TOC link on scroll ────────────────────────────────────────── */
(function initTocHighlight() {
  const tocLinks = document.querySelectorAll('.toc-nav a[data-anchor]');
  if (!tocLinks.length) return;

  const anchors = Array.from(tocLinks).map(link => {
    const el = document.getElementById(link.dataset.anchor);
    return { link, el };
  }).filter(x => x.el);

  let raf;
  function highlight() {
    const scrollY = window.scrollY + 100; // offset for header
    let current = anchors[0];
    for (const item of anchors) {
      const top = item.el.getBoundingClientRect().top + window.scrollY;
      if (scrollY >= top) current = item;
    }
    if (current) {
      tocLinks.forEach(l => l.classList.remove('active'));
      current.link.classList.add('active');
      // Scroll the TOC sidebar so the active link is visible
      const tocNav = document.getElementById('tocNav');
      if (tocNav) {
        const linkOffset = current.link.offsetTop - tocNav.scrollTop - tocNav.clientHeight / 2;
        if (Math.abs(linkOffset) > 80) {
          tocNav.scrollBy({ top: linkOffset, behavior: 'smooth' });
        }
      }
    }
  }

  window.addEventListener('scroll', () => {
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(highlight);
  }, { passive: true });
  highlight(); // initial call
})();

/* ── Mobile TOC sidebar toggle ────────────────────────────────────────── */
function toggleToc() {
  const sidebar = document.getElementById('tocSidebar');
  sidebar.classList.toggle('open');
}
// Close TOC when clicking outside on mobile
document.addEventListener('click', function(e) {
  const sidebar = document.getElementById('tocSidebar');
  const toggleBtn = document.getElementById('btnTocToggle');
  if (!sidebar || !toggleBtn) return;
  if (sidebar.classList.contains('open')
      && !sidebar.contains(e.target)
      && !toggleBtn.contains(e.target)) {
    sidebar.classList.remove('open');
  }
});
// Close TOC when a link is clicked on mobile
document.querySelectorAll('.toc-nav a').forEach(link => {
  link.addEventListener('click', () => {
    const sidebar = document.getElementById('tocSidebar');
    if (window.innerWidth < 820 && sidebar) sidebar.classList.remove('open');
  });
});

/* ── Smooth scroll offset for fixed header ────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const id = this.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      const hdrH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hdr-h')) || 56;
      const y = target.getBoundingClientRect().top + window.scrollY - hdrH - 12;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  });
});

/* ── Interactive Code Cell Execution ─────────────────────────────────── */
function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function runCell(btn) {
  const article = btn.closest('.nb-cell');
  if (!article) return;
  const pre = article.querySelector('.hl pre');
  if (!pre) return;
  const code = pre.innerText;

  const origHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `<span class="spin-icon">⏳</span> Ejecutando...`;

  let liveOut = article.querySelector('.live-output');
  if (!liveOut) {
    liveOut = document.createElement('div');
    liveOut.className = 'live-output';
    article.appendChild(liveOut);
  }
  liveOut.innerHTML = `
    <div class="live-out-header">
      <span class="live-tag">⚡ Ejecución en Python...</span>
    </div>
    <div class="live-out-loading">Ejecutando celda...</div>
  `;

  fetch('/api/run_cell', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: code })
  })
  .then(res => {
    if (!res.ok) {
      return res.json().then(err => { throw new Error(err.error || `HTTP ${res.status}`); });
    }
    return res.json();
  })
  .then(data => {
    btn.disabled = false;
    btn.innerHTML = origHtml;

    const isSuccess = (data.exit_code === 0);
    const statusTag = isSuccess
      ? '<span class="live-status-ok">✓ Éxito (0)</span>'
      : `<span class="live-status-err">✗ Error (${data.exit_code})</span>`;

    let outContent = '';
    if (data.stdout) {
      outContent += `<pre class="nb-out out-stdout">${escapeHtml(data.stdout)}</pre>`;
    }
    if (data.stderr) {
      outContent += `<pre class="nb-out out-stderr">${escapeHtml(data.stderr)}</pre>`;
    }
    if (!data.stdout && !data.stderr) {
      outContent = '<div class="live-out-empty">✓ La celda se ejecutó correctamente sin salida en consola.</div>';
    }

    liveOut.innerHTML = `
      <div class="live-out-header">
        <span class="live-tag">⚡ Salida interactiva</span>
        ${statusTag}
      </div>
      <div class="live-out-body">
        ${outContent}
      </div>
    `;
  })
  .catch(err => {
    btn.disabled = false;
    btn.innerHTML = origHtml;
    liveOut.innerHTML = `
      <div class="live-out-header">
        <span class="live-tag live-tag-err">⚠ Error de ejecución</span>
      </div>
      <pre class="nb-out out-error"><b>Error:</b> ${escapeHtml(err.message)}</pre>
    `;
  });
}

