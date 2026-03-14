/**
 * Identity
 *
 * Generates and persists a per-browser user ID in localStorage.
 * All members are static — use Identity.get() directly.
 */
export default class Identity {
  static #uid = null;

  static get() {
    if (Identity.#uid) return Identity.#uid;

    Identity.#uid = localStorage.getItem('sb_uid');
    if (!Identity.#uid) {
      Identity.#uid = 'u_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
      localStorage.setItem('sb_uid', Identity.#uid);
    }

    return Identity.#uid;
  }
}
