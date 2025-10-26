import { API_BASE_URL } from "../config";

async function PutProfile(token: string, userId: string, formData: FormData) {
	return fetch(`${API_BASE_URL}/accounts/profiles/${userId}/`, {
		method: 'PUT',
		headers: {
			'Authorization': `Bearer ${token}`,
		},
		body: formData,
	});
}

export default PutProfile;