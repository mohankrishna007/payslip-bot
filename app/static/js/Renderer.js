/**
 * Renderer
 *
 * Converts raw text into safe HTML for display inside chat bubbles.
 * Handles bot-specific rich markup (section headers, salary tables,
 * tip/warning callouts) as well as plain user messages.
 * All members are static — pure transformation, no side effects.
 */
export default class Renderer {
  static #esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  static #inl(t) {
    return t
      .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
      .replace(/_(.*?)_/g,   '<em>$1</em>');
  }

  /** Convert raw bot response text to bubble-safe HTML. */
  static renderBot(raw) {
    const lines = Renderer.#esc(raw).split('\n');
    const out   = [];

    for (let i = 0; i < lines.length; i++) {
      const ln = lines[i];
      const tr = ln.trim();

      // Horizontal divider
      if (/^[─━\-]{5,}$/.test(tr)) {
        out.push('<div class="divider"></div>');
        continue;
      }

      // Callout lines
      if (tr.startsWith('💡')) {
        out.push(`<span class="tip-line">💡 ${Renderer.#inl(tr.slice('💡'.length).trim())}</span>`);
        continue;
      }
      if (tr.startsWith('⚠️')) {
        out.push(`<span class="warn-line">⚠️ ${Renderer.#inl(tr.slice('⚠️'.length).trim())}</span>`);
        continue;
      }

      // Salary summary block (Gross earned / Total deducted rows + net)
      if (/^(Gross earned|Total deducted)\s+₹/.test(tr)) {
        const rows = [];
        while (i < lines.length && /^(Gross earned|Total deducted)\s+₹/.test(lines[i].trim()))
          rows.push(lines[i++]);
        while (i < lines.length && lines[i].trim() === '') i++;
        let net = '';
        if (i < lines.length && lines[i].includes('In your account')) net = lines[i++];
        i--;
        let b = '<div class="nums-block">' + rows.map(r => Renderer.#inl(r.trim()) + '<br>').join('');
        if (net) b += `<div class="net-row">${Renderer.#inl(net.trim())}</div>`;
        out.push(b + '</div>');
        continue;
      }

      // Section headers  (*TEXT*  at end of line, no em-dash after)
      if (/\*[^*]+\*\s*$/.test(tr) && !/^\*[^*]+\*\s*[—–]/.test(tr)) {
        out.push(`<span class="section-head">${Renderer.#inl(tr)}</span>`);
        continue;
      }

      // Component headers  (*TEXT*  at start of line)
      if (/^\*[^*]+\*/.test(tr)) {
        out.push(`<span class="comp-header">${Renderer.#inl(tr)}</span>`);
        continue;
      }

      // Blank line → spacing gap
      if (tr === '') { out.push('<br>'); continue; }

      out.push(Renderer.#inl(tr) + '<br>');
    }

    return out.join('');
  }

  /** Escape and line-break a plain user message for display. */
  static renderUser(text) {
    return Renderer.#esc(text).replace(/\n/g, '<br>');
  }
}
