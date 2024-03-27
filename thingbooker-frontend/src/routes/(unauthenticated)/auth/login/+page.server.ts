import api from '$lib/utils/backend';
import { fail, redirect } from '@sveltejs/kit';
import { setCookie } from '$lib/utils/auth.js';

export const actions = {
  login: async ({ cookies, request, url }) => {
    const formData = await request.formData();
    const username = formData.get('email');
    const password = formData.get('password');
    if (!username) {
      return fail(400, { email: username, error: 'Vennligst skriv inn din e-postadresse' });
    }

    if (!password) {
      return fail(400, { email: username, error: 'Vennligst skriv inn ditt passord' });
    }

    const response = await api.auth.loginUser(username.toString(), password.toString());
    if (200 <= response.status && response.status < 300) {
      for (const cookie of response.headers.getSetCookie()) {
        setCookie(cookies, cookie);
      }
      const next = url.searchParams.get('next');
      const redirectUrl = next ? next : '/tb';
      redirect(303, redirectUrl);
    }
    return fail(400, { email: username, error: 'E-postadressen din eller passordet ditt er feil' });
  }
};
