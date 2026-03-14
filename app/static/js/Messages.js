import Renderer from './Renderer.js';

/**
 * Messages
 *
 * Manages the chat message feed: appends bot/user bubbles and
 * controls the animated typing indicator.
 * Instantiate once and share the instance across the app.
 */
export default class Messages {
  #feed;

  constructor() {
    this.#feed = document.getElementById('messages');
  }

  #nowStr() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  /** Append a chat bubble to the feed. */
  add(text, role) {
    const row  = document.createElement('div'); row.className = `row ${role}`;
    const wrap = document.createElement('div'); wrap.className = 'bubble-wrap';
    const bub  = document.createElement('div'); bub.className = `bubble ${role}`;

    bub.innerHTML = role === 'bot'
      ? Renderer.renderBot(text)
      : Renderer.renderUser(text);

    const ts = document.createElement('div');
    ts.className = 'ts';
    ts.textContent = this.#nowStr();

    wrap.append(bub, ts);
    row.append(wrap);
    this.#feed.appendChild(row);
    this.#feed.scrollTop = this.#feed.scrollHeight;
  }

  /** Show the animated typing indicator while awaiting a response. */
  showTyping() {
    const row = document.createElement('div');
    row.className = 'row bot';
    row.id        = 'typing-row';
    row.innerHTML = '<div class="bubble-wrap"><div class="typing"><span></span><span></span><span></span></div></div>';
    this.#feed.appendChild(row);
    this.#feed.scrollTop = this.#feed.scrollHeight;
  }

  /** Remove the typing indicator. */
  removeTyping() {
    document.getElementById('typing-row')?.remove();
  }
}
