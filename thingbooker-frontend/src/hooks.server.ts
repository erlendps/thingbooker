import { isAuthenticated, refreshAccessToken, isProtectedPage } from '$lib/utils/auth';

/** @type {import('@sveltejs/kit').Handle}
 * \
 * \
 * Handles the request made to server.
 *
 * The handle will check if the user is authenticated before resolving the request.
 * If the user is not authenticated, it will then try to reacquire the access token.
 * If this also fails, the user is redirected back to the login page.
 *
 * The input parameter is an object of the two parameters described under.
 *
 * @param event The request event from the client
 * @param resolve returns a promise that will resolve the request
 * @returns If awaited, the handle returns the response for the request
 */
export async function handle({ event, resolve }) {
  // check if the route is protected
  const route = event.route.id;
  if (route && isProtectedPage(route)) {
    if (!isAuthenticated(event.cookies)) {
      // not a valid access token
      if (!(await refreshAccessToken(event.cookies)))
        // not a valid refresh token either
        return new Response('Redirect', { status: 303, headers: { Location: '/login' } });
    }
  }
  return await resolve(event);
}

/** @type {import('@sveltejs/kit').HandleFetch}
 * \
 * \
 * Handles fetch calls made by the server.
 *
 * The handle will inject the authorization header when trying to access
 * protected views.
 */
export async function handleFetch({ event, request, fetch }) {
  return fetch(request);
}
