import { reauthenticateIfUnauthenticated } from '$lib/utils/auth';

/** @type {import('./$types').LayoutServerLoad} */
export async function load({ cookies }) {
  const isAuthenticated = await reauthenticateIfUnauthenticated(cookies);

  if (isAuthenticated) {
    //
  }

  return {
    isAuthenticated: isAuthenticated
  };
}
