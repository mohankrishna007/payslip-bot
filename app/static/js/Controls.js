import AppState from './AppState.js';

/**
 * Controls
 *
 * Enables or disables the interactive UI elements as a group,
 * and provides the auto-resize helper for the message textarea.
 * All members are static — no instantiation required.
 */
export default class Controls {
  /** Disable (on=true) or re-enable (on=false) input controls. */
  static setDisabled(on) {
    document.getElementById('msg-input').disabled = on;
    document.getElementById('send-btn').disabled  = on;

    const state     = AppState.current();
    const canUpload = state === 'AWAITING_FILE' || state === 'CHAT';
    document.getElementById('upload-btn').disabled = on || !canUpload;
  }

  /** Grow the textarea to fit its content (up to CSS max-height). */
  static autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
  }
}
