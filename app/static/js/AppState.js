/**
 * AppState
 *
 * Manages the server-driven session state: updates the status pill,
 * toggles the upload button, and shows/hides the upload hint bar.
 * All members are static — use AppState.apply() / AppState.current()
 * directly.
 */
export default class AppState {
  static #state = 'INIT';

  static apply(state) {
    AppState.#state = state;

    const canUpload = state === 'AWAITING_FILE' || state === 'CHAT';
    document.getElementById('upload-btn').disabled = !canUpload;

    const hint = document.getElementById('upload-hint');
    if (canUpload) {
      hint.textContent  = '📎 Click the clip icon or drag a payslip here  ·  JPEG · PNG · PDF';
      hint.style.display = 'block';
    } else {
      hint.style.display = 'none';
    }
  }

  static current() { return AppState.#state; }
}
