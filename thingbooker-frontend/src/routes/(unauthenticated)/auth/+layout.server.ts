import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ parent }) {
  const { isAuthenticated } = await parent();
  if (isAuthenticated) redirect(303, '/tb');
}
