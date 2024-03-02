import type { Cookies } from '@sveltejs/kit';
import { BACKEND_URL } from './constants';
import { dev } from '$app/environment';

/**
 * Checks if the user is authenticated.
 *
 * It checks wheter the cookie 'thingbooker-access-token' is present
 * in the user's browser.
 *
 * @param cookies svelte cookies api
 * @returns
 */
export const isAuthenticated = (cookies: Cookies) => {
  // Since there is no way to explicitly check expiry date, I assume it's deleted once
  // it's expired

  // convert to boolean
  return !!cookies.get('thingbooker-access-token');
};

/**
 * Tries to refresh the access token.
 *
 * @param cookies svelte cookies api
 * @returns `true` if the access token was successfully refreshed, `false` otherwise.
 */
export const refreshAccessToken = async (cookies: Cookies) => {
  const refreshToken = cookies.get('thingbooker-refresh-token');

  if (!refreshToken) {
    // user needs to login again
    return false;
  }
  const formData = new FormData();
  formData.append('refresh', refreshToken);
  const response = await fetch(BACKEND_URL + 'auth/token/refresh/', {
    method: 'POST',
    body: formData
  });
  if (200 <= response.status && response.status < 300) {
    response.headers
      .getSetCookie()
      .forEach((setCookieString) => setCookie(cookies, setCookieString));

    return true;
  }

  return false;
};

/**
 * Sets a cookie based on the data gathered from cookieString.
 *
 * @param cookies svelte cookies api
 * @param cookieString a string describing a cookie
 */
export const setCookie = (cookies: Cookies, cookieString: string) => {
  const cookieData = parseCookie(cookieString);
  const cookieName = cookieData['name'];
  cookies.set(cookieName, cookieData[cookieName], {
    path: cookieData['Path'],
    expires: new Date(cookieData['expires']),
    maxAge: parseInt(cookieData['Max-Age']),
    sameSite: 'lax',
    secure: !dev
  });
};

/**
 * Parses a cookie string to an object with key-value pairs.
 *
 * @param cookie string that describes a cookie
 * @returns An object with key-value pairs corresponding to the cookie string
 */
export const parseCookie = (cookie: string): Record<string, string> => {
  const name = cookie.split(';')[0].split('=')[0];

  return cookie
    .split(';')
    .map((v) => v.split('='))
    .reduce(
      (acc: Record<string, string>, v) => {
        acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
        return acc;
      },
      { name: name }
    );
};
