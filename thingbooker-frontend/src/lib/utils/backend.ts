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
  AUTH_URL,
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

const ACCOUNTS_URL = BACKEND_URL + 'accounts/';
const accounts = {
  ACCOUNTS_URL,
  getAllKnownUsers: async (short: boolean = false) => {
    return await fetch(ACCOUNTS_URL + `?short=${short}`);
  },
  getUserById: async (userId: string, short: boolean = false) => {
    return await fetch(ACCOUNTS_URL + `${userId}/?short=${short}`);
  }
};

const GROUPS_URL = BACKEND_URL + 'groups/';
const TOKENS_URL = BACKEND_URL + 'invite-tokens';
const groups = {
  GROUPS_URL,
  TOKENS_URL,
  /**
   * Fetches all the groups the user knows.
   *
   * @returns response from backend
   */
  getAllKnownGroups: async () => {
    return await fetch(GROUPS_URL);
  },
  /**
   * Fetches a group by id. If the group is not 'known' to the user, 404 is returned
   *
   * @param groupId
   * @returns response from backend
   */
  getGroupById: async (groupId: string) => {
    return await fetch(GROUPS_URL + `${groupId}/`);
  },
  /**
   * Deletes the given group. Only the owner can do this.
   *
   * @param groupId
   * @returns response from backend
   */
  deleteGroup: async (groupId: string) => {
    return await fetch(GROUPS_URL + `${groupId}/`, { method: 'DELETE' });
  },
  /**
   * Creates a new group with owner set as the current user.
   *
   * @param name
   * @param groupPicture
   * @returns response from backend
   */
  createGroup: async (name: string, groupPicture?: File) => {
    const data = createFormData({ name, group_picture: groupPicture });

    return await fetch(GROUPS_URL, { method: 'POST', body: data });
  },
  /**
   * Updates the group with corresponding groupId. Only the owner can do this
   *
   * @param groupId
   * @param param1
   * @returns response from backend
   */
  updateGroup: async (
    groupId: string,
    { name, groupPicture }: { name?: string; groupPicture?: File }
  ) => {
    const data = createFormData({ name, group_picture: groupPicture });

    return await fetch(GROUPS_URL + `${groupId}/`, { method: 'PATCH', body: data });
  },
  /**
   * Invites a thingbooker user to the group, if the user exists.
   *
   * @param groupId
   * @param email email of the user being invited
   * @returns response from backend
   */
  inviteMemberToGroup: async (groupId: string, email: string) => {
    const data = createFormData({ email });

    return await fetch(GROUPS_URL + `${groupId}/invite_member/`, { method: 'POST', body: data });
  },
  /**
   * Accepts a group invite.
   *
   * @param token
   * @returns response from backend
   */
  acceptGroupInvite: async (token: string) => {
    return await fetch(TOKENS_URL + `accept-invite/${token}/`, { method: 'POST' });
  },
  /**
   * Fetches a list of all invite tokens. Only a admin can do this.
   *
   * @returns response from backend
   */
  getAllInviteTokens: async () => {
    return await fetch(TOKENS_URL);
  },
  /**
   * Fetches the token with the given tokenId. Only an admin can do this.
   *
   * @param tokenId
   * @returns response from backend
   */
  getInviteToken: async (tokenId: string) => {
    return await fetch(TOKENS_URL + `${tokenId}/`);
  }
};

const THINGS_URL = BACKEND_URL + 'things/';
const things = { THINGS_URL };

const BOOKINGS_URL = BACKEND_URL + 'bookings/';
const bookings = { BOOKINGS_URL };

const RULES_URL = BACKEND_URL + 'rules/';
const rules = { RULES_URL };

const api = {
  accounts,
  auth,
  bookings,
  groups,
  rules,
  things
};

export default api;
