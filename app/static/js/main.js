/**
 * main.js — application entry point
 *
 * Imports all modules, wires up event listeners, then boots the app
 * by fetching the current session state and greeting the user.
 */

import QRPanel   from './QRPanel.js';
import QROverlay from './QROverlay.js';
import Identity  from './Identity.js';
import AppState  from './AppState.js';
import Messages  from './Messages.js';
import API       from './API.js';
import Controls  from './Controls.js';
import Chat      from './Chat.js';

// ── Instantiate instance-based classes ──────────────────────────────────
const messages  = new Messages();
const overlay   = new QROverlay();
const chat      = new Chat(messages);

// ── Event bindings ───────────────────────────────────────────────────────
const input = document.getElementById('msg-input');
input.addEventListener('input',   function () { Controls.autoResize(this); });
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); chat.send(); }
});

document.getElementById('send-btn')
  .addEventListener('click', () => chat.send());

document.getElementById('file-input')
  .addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;
    this.value = '';
    chat.upload(file);
  });

document.getElementById('upload-btn')
  .addEventListener('click', () => document.getElementById('file-input').click());

// Drag-and-drop onto the entire shell
const shell = document.getElementById('shell');
shell.addEventListener('dragover',  e => { e.preventDefault(); shell.style.outline = '2px dashed var(--brand)'; });
shell.addEventListener('dragleave', ()  => { shell.style.outline = ''; });
shell.addEventListener('drop', e => {
  e.preventDefault();
  shell.style.outline = '';
  const file = e.dataTransfer?.files?.[0];
  if (!file) return;
  const fi = document.getElementById('file-input');
  const dt = new DataTransfer();
  dt.items.add(file);
  fi.files = dt.files;
  fi.dispatchEvent(new Event('change'));
});

// ── Boot ─────────────────────────────────────────────────────────────────
QRPanel.init();
overlay.init();
Controls.setDisabled(true);

try {
  const session = await API.getSession(Identity.get());
  AppState.apply(session.state);

  if (session.state === 'INIT' || session.state === 'AWAITING_CONSENT') {
    messages.showTyping();
    const data = await API.postJSON('/app/message', { user_id: Identity.get(), text: 'hi' });
    messages.removeTyping();
    messages.add(data.reply, 'bot');
    AppState.apply(data.state);

  } else if (session.state === 'CHAT') {
    messages.add(
      session.has_session
        ? '👋 Welcome back! Your session is still active.\n\nAsk me anything, or type *reset* to start over.'
        : '👋 Welcome back! Your last session has expired.\n\nType *reset* to upload a new payslip.',
      'bot'
    );

  } else if (session.state === 'AWAITING_FILE') {
    messages.add('📎 Welcome back — please upload your payslip to continue.', 'bot');
  }

} catch {
  messages.add('⚠️ Could not connect to the server. Is it running?', 'bot');

} finally {
  Controls.setDisabled(false);
  document.getElementById('msg-input').focus();
}
