import { BACKEND_URL } from './constants';

const login = async (username: string, password: string) => {
  const data = new FormData();
  data.append('username', username);
  data.append('password', password);

  return await fetch(BACKEND_URL + 'auth/login/', { method: 'POST', body: data });
};

const api = {
  loginUser: login
};

export default api;
