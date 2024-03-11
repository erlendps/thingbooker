import { BACKEND_URL } from './constants';

const createFormData = ({ ...fields }) => {
  const data = new FormData();
  for (const [field, value] of Object.entries(fields)) {
    data.append(field, value);
  }
  return data;
};

const api = {
  loginUser: async (username: string, password: string) => {
    const data = createFormData({ username: username, password: password });

    return await fetch(BACKEND_URL + 'auth/login/', { method: 'POST', body: data });
  }
};

export default api;
