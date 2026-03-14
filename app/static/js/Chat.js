import Identity from './Identity.js';
import AppState  from './AppState.js';
import API       from './API.js';
import Controls  from './Controls.js';

/**
 * Chat
 *
 * Orchestrates the send-message and file-upload flows:
 * reads user input → calls the backend → updates the feed and state.
 *
 * Requires a Messages instance injected at construction time.
 */
export default class Chat {
  #messages;

  constructor(messages) {
    this.#messages = messages;
  }

  /** Read the textarea, POST to /app/message, render the reply. */
  async send() {
    const inp = document.getElementById('msg-input');
    const txt = inp.value.trim();
    if (!txt || inp.disabled) return;

    inp.value = '';
    Controls.autoResize(inp);
    this.#messages.add(txt, 'user');
    Controls.setDisabled(true);
    this.#messages.showTyping();

    try {
      const data = await API.postJSON('/app/message', {
        user_id: Identity.get(),
        text:    txt,
      });
      this.#messages.removeTyping();
      this.#messages.add(data.reply, 'bot');
      AppState.apply(data.state);
    } catch {
      this.#messages.removeTyping();
      this.#messages.add('⚠️ Network error — please try again.', 'bot');
    } finally {
      Controls.setDisabled(false);
      document.getElementById('msg-input').focus();
    }
  }

  /** Upload a payslip file, POST to /app/upload, render the reply. */
  async upload(file) {
    this.#messages.add(`📎 Uploading: ${file.name}`, 'user');
    Controls.setDisabled(true);
    this.#messages.showTyping();

    const fd = new FormData();
    fd.append('user_id', Identity.get());
    fd.append('file',    file);

    try {
      const data = await API.postForm('/app/upload', fd);
      this.#messages.removeTyping();
      this.#messages.add(data.reply, 'bot');
      AppState.apply(data.state);
    } catch {
      this.#messages.removeTyping();
      this.#messages.add('⚠️ Upload failed — please try again.', 'bot');
    } finally {
      Controls.setDisabled(false);
    }
  }
}
