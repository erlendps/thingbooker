export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const unprotectedPages: string = import.meta.env.VITE_UNPROTECTED_PAGES;
export const UNPROTECTED_PAGES = unprotectedPages.split(',');
export const BASE_LOGGEDIN_URL = '/tb';
