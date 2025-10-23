import { API_BASE_URL } from './config';


async function fetchRefresh(token: string) {
	const res = await fetch(`${API_BASE_URL}/tokens/refresh/`, {
	method: 'POST',
	headers: { 'Content-Type': 'application/json' },
	body: JSON.stringify({ refresh: token }),
	});
	if (res.ok) {
	const data = await res.json();
	localStorage.setItem('access_token', data.access);
	} else {
		localStorage.removeItem('access_token');
		localStorage.removeItem('refresh_token');
	}
}

export default fetchRefresh;
