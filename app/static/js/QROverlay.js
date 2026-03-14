/**
 * QROverlay
 *
 * Controls the mobile / tablet bottom-sheet that shows the QR panel
 * when the desktop sidebar is hidden. Instantiate once and call init().
 */
export default class QROverlay {
  #overlay;

  constructor() {
    this.#overlay = document.getElementById('qr-overlay');
  }

  open() {
    this.#overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.#overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  /** Attach all event listeners required to open / close the overlay. */
  init() {
    document.getElementById('wa-toggle')
      .addEventListener('click', () => this.open());

    document.getElementById('qr-close')
      .addEventListener('click', () => this.close());

    // Tap outside the sheet to dismiss
    this.#overlay.addEventListener('click', e => {
      if (e.target === this.#overlay) this.close();
    });

    // Keyboard accessibility
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') this.close();
    });
  }
}
