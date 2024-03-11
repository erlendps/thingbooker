import { BACKEND_URL } from './constants';

const createFormData = ({ ...fields }) => {
  const data = new FormData();
  for (const [field, value] of Object.entries(fields)) {
    if (typeof value === 'undefined') continue;
    data.append(field, value);
  }

  return data;
};

const AUTH_URL = BACKEND_URL + 'auth/';

const auth = {
  /**
   * Tries to log in using the credentials provided.
   *
   * @param username
   * @param password
   * @returns response from backend
   */
  loginUser: async (username: string, password: string) => {
    const data = createFormData({ username, password });

    return await fetch(AUTH_URL + 'login/', { method: 'POST', body: data });
  },
  /**
   * Logs the user out but blacklisting the refresh token.
   *
   * @param refreshToken
   * @returns response from backend
   */
  logoutUser: async (refreshToken: string) => {
    const data = createFormData({ refresh: refreshToken });

    return await fetch(AUTH_URL + 'logout/', { method: 'POST', body: data });
  },
  /**
   * Registers a new user to thingbooker. Avatar is optional.
   *
   * @param username
   * @param password1
   * @param password2
   * @param firstName
   * @param lastName
   * @param avatar
   * @returns response from backend.
   */
  registerUser: async (
    username: string,
    password1: string,
    password2: string,
    firstName: string,
    lastName: string,
    avatar?: File
  ) => {
    const dataObject = {
      username,
      password1,
      password2,
      first_name: firstName,
      last_name: lastName,
      avatar
    };
    const data = createFormData(dataObject);

    return await fetch(AUTH_URL + 'registration/', { method: 'POST', body: data });
  },
  /**
   * Requests resetting the password associated to the given email/username.
   *
   * @param email
   * @returns response from backend.
   */
  requestResetPassword: async (email: string) => {
    const data = createFormData({ email });

    return await fetch(AUTH_URL + 'password/reset/', { method: 'POST', body: data });
  },
  /**
   * Sets a new password for the user with the uid and token.
   *
   * @param uid
   * @param token
   * @param newPassword1
   * @param newPassword2
   * @returns response from backend
   */
  resetPassword: async (uid: string, token: string, newPassword1: string, newPassword2: string) => {
    const data = createFormData({
      uid,
      token,
      new_password1: newPassword1,
      new_password2: newPassword2
    });

    return await fetch(AUTH_URL + 'password/reset/confirm/', { method: 'POST', body: data });
  },
  /**
   * Changes the password for the user.
   *
   * @param oldPassword
   * @param newPassword1
   * @param newPassword2
   * @returns response from backend
   */
  changePassword: async (oldPassword: string, newPassword1: string, newPassword2: string) => {
    const data = createFormData({
      old_password: oldPassword,
      new_password1: newPassword1,
      new_password2: newPassword2
    });

    return await fetch(AUTH_URL + 'password/change/', { method: 'POST', body: data });
  },
  /**
   * Tries to get the current user by looking at the access token.
   *
   * Note that in src/hooks.server.ts there is a custom handleFetch override
   * that will inject the authorization header on requests.
   *
   * @returns response from backend
   */
  getCurrentUser: async () => {
    return await fetch(AUTH_URL + 'user/', { method: 'GET' });
  },
  /**
   * Does a partial update of the current user.
   *
   * @param object Since everything is optional, we have to use an object here so we can
   * have named parameters.
   *
   * The possible fields to update are:
   * @param firstName
   * @param lastName
   * @param avatar
   *
   * @returns response from backend
   */
  updateCurrentUser: async ({
    firstName,
    lastName,
    avatar
  }: {
    firstName?: string;
    lastName?: string;
    avatar?: File;
  }) => {
    const data = createFormData({ first_name: firstName, last_name: lastName, avatar });

    return await fetch(AUTH_URL + 'user/', { method: 'PATCH', body: data });
  },
  /**
   * Checks if the supplied token is valid.
   *
   * The token can either be an access token or a refresh token.
   *
   * @param token
   * @returns response from backend
   */
  verifyToken: async (token: string) => {
    const data = createFormData({ token });

    return await fetch(AUTH_URL + 'token/verify/', { method: 'POST', body: data });
  },
  /**
   * Refreshes the token using the refresh token.
   *
   * @param refreshToken
   * @returns response from backend. A cookie or similar should be set to persist connection
   */
  refreshAccessToken: async (refreshToken: string) => {
    const data = createFormData({ refresh: refreshToken });

    return await fetch(AUTH_URL + 'token/refresh/', { method: 'POST', body: data });
  }
};

const api = {
  auth
};

export default api;
