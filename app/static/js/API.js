/**
 * API
 *
 * Thin fetch wrappers for the SalaryBuddy backend endpoints.
 * All members are static — no instantiation required.
 */
export default class API {
  /** POST JSON body, return parsed response. */
  static async postJSON(path, body) {
    const res = await fetch(path, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
    });
    if (!res.ok) throw new Error(res.status);
    return res.json();
  }

  /** POST multipart/form-data (file upload), return parsed response. */
  static async postForm(path, formData) {
    const res = await fetch(path, { method: 'POST', body: formData });
    if (!res.ok) throw new Error(res.status);
    return res.json();
  }

  /** GET the current session state for a user. */
  static async getSession(userId) {
    const res = await fetch(`/app/session/${userId}`);
    if (!res.ok) throw new Error(res.status);
    return res.json();
  }
}
