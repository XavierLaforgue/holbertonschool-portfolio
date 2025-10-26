import { API_BASE_URL } from '../config';


async function fetchWithRefresh(url: string, accessToken: string, options: RequestInit = {}) {
  let res = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`,
    },
  });

  if (res.status === 401) {
    const refreshToken = localStorage.getItem('refresh_token');
    const refreshRes = await fetch(`${API_BASE_URL}/tokens/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    if (refreshRes.ok) {
      const data = await refreshRes.json();
      localStorage.setItem('access_token', data.access);
      accessToken = data.access;
      res = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${accessToken}`,
        },
      });
    } else {
      localStorage.removeItem('access_token');
      return null;
    }
  }
  return res;
}

export default fetchWithRefresh;
