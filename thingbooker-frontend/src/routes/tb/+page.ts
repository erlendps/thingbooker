import { redirect } from '@sveltejs/kit';
/** @type {import('./$types').PageLoad}
 * \
 * \
 * The load function for /tb always redirect to /tb/things
 */
export function load() {
  redirect(301, '/tb/things');
}
