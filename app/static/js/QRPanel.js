/**
 * QRPanel
 *
 * Builds the placeholder QR canvas and populates the `.qr-inner`
 * containers inside both the desktop sidebar (#qr-panel) and the
 * mobile bottom-sheet (#qr-overlay) from a single source of truth.
 * All methods are static — no instantiation needed.
 */
export default class QRPanel {
  static #STEPS = [
    ['1', 'Open <strong style="color:var(--brand)">WhatsApp</strong> and tap the new chat icon'],
    ['2', 'Tap the <strong style="color:var(--brand)">QR / camera</strong> icon and scan this code'],
    ['3', 'Send any message — SalaryBuddy will guide you from there'],
  ];

  /** Draw a placeholder QR-code pattern onto a canvas element. */
  static #buildCanvas() {
    const canvas = document.createElement('canvas');
    canvas.className = 'qr-canvas';
    canvas.width = 130; canvas.height = 130;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, N = 25, cs = W / N;
    const m = Array.from({ length: N }, () => new Array(N).fill(0));

    // Finder patterns (three corners)
    const finder = (tr, tc) => {
      for (let r = 0; r < 7; r++)
        for (let c = 0; c < 7; c++)
          m[tr+r][tc+c] = (r===0||r===6||c===0||c===6||(r>=2&&r<=4&&c>=2&&c<=4)) ? 1 : 0;
    };
    finder(0,0); finder(0,18); finder(18,0);

    // Timing patterns
    for (let i = 8; i <= 16; i++) { m[6][i] = i%2===0?1:0; m[i][6] = i%2===0?1:0; }

    // Alignment pattern
    for (let r = 0; r < 5; r++)
      for (let c = 0; c < 5; c++)
        m[16+r][16+c] = (r===0||r===4||c===0||c===4||(r===2&&c===2)) ? 1 : 0;

    m[13][8] = 1;

    // Protected zones (finder + timing + alignment)
    const forbidden = new Set();
    for (let r=0;r<8;r++) for (let c=0;c<8;c++)    forbidden.add(r*N+c);
    for (let r=0;r<8;r++) for (let c=17;c<25;c++)  forbidden.add(r*N+c);
    for (let r=17;r<25;r++) for (let c=0;c<8;c++)  forbidden.add(r*N+c);
    for (let i=0;i<N;i++) { forbidden.add(6*N+i); forbidden.add(i*N+6); }
    for (let r=15;r<21;r++) for (let c=15;c<21;c++) forbidden.add(r*N+c);

    // Deterministic pseudo-random fill for the data area
    let s = 0xab12ef34;
    const rng = () => { s=(s^s<<13)>>>0; s=(s^s>>17)>>>0; s=(s^s<<5)>>>0; return (s>>>0)/0xffffffff; };
    for (let r=0;r<N;r++)
      for (let c=0;c<N;c++)
        if (!forbidden.has(r*N+c)) m[r][c] = rng()>.5?1:0;

    ctx.fillStyle = '#fff'; ctx.fillRect(0,0,W,W);
    ctx.fillStyle = '#1e1b4b';
    for (let r=0;r<N;r++)
      for (let c=0;c<N;c++)
        if (m[r][c]) ctx.fillRect(c*cs+.5, r*cs+.5, cs-.5, cs-.5);

    return canvas;
  }

  /** Fill a `.qr-inner` container with QR card content. */
  static #populateInner(container) {
    container.innerHTML = '';

    const brand = document.createElement('div');
    brand.className = 'qr-brand';
    brand.innerHTML = `
      <div class="qr-brand-mark">💼</div>
      <div class="qr-brand-text">
        <strong>SalaryBuddy</strong><span>Also on WhatsApp</span>
      </div>`;

    const intro = document.createElement('p');
    intro.className = 'qr-intro';
    intro.innerHTML = 'Prefer doing this on your phone?<br>Scan to continue on WhatsApp.';

    const card = document.createElement('div');
    card.className = 'qr-card';
    const cardTitle = document.createElement('div');
    cardTitle.className = 'qr-card-title';
    cardTitle.textContent = 'WhatsApp Channel';
    const badge = document.createElement('div');
    badge.className = 'qr-test-badge';
    badge.textContent = '⚙️ Test QR — setup pending';
    card.append(cardTitle, QRPanel.#buildCanvas(), badge);

    const sep = document.createElement('div');
    sep.className = 'qr-sep';
    sep.textContent = 'How to scan';

    const steps = document.createElement('div');
    steps.className = 'qr-steps';
    for (const [n, html] of QRPanel.#STEPS) {
      const row = document.createElement('div');
      row.className = 'step';
      row.innerHTML = `<div class="step-n">${n}</div><span>${html}</span>`;
      steps.appendChild(row);
    }

    const privacy = document.createElement('p');
    privacy.className = 'qr-privacy';
    privacy.innerHTML = '🔒 Your payslip is never stored with your identity.<br>All personal info is scrubbed before processing.';

    container.append(brand, intro, card, sep, steps, privacy);
  }

  /** Populate all `.qr-inner` elements found in the document. */
  static init() {
    document.querySelectorAll('#qr-panel .qr-inner, #qr-overlay .qr-inner')
      .forEach(el => QRPanel.#populateInner(el));
  }
}
