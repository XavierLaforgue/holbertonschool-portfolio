import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';
import PopUpModal from '../components/PopUpModal';
import { useNavigate } from 'react-router-dom';
import '../styles/UpdateProfilePage.css';
import parseDjangoError from '../parseDjangoError';
import { useAuth } from '../context/useAuth';
import fetchWithRefresh from '../functions/fetchWithRefresh';


const UpdateProfilePage: React.FC = () => {
	const { user, setUser } = useAuth();
	const navigate = useNavigate();

	const [form, setForm] = useState({
		bio: '',
		favorite_anime: '',
		favorite_meal: '',
		location: '',
		personal_website: '',
		dietary_preferences: '',
	});
	const [avatar, setAvatar] = useState<File | null>(null);
	const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
	const [error, setError] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [showErrorModal, setShowErrorModal] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const [profileLoading, setProfileLoading] = useState(true);

	// Redirect if not authenticated
	useEffect(() => {
		if (!isLoading && !user) {
			console.log('[UpdateProfilePage] No user found, redirecting to login');
			navigate('/login');
		}
	}, [isLoading, user, navigate]);

	// Fetch existing profile data
	useEffect(() => {
		if (!user) return;

		const fetchProfile = async () => {
			console.log('[UpdateProfilePage] Fetching profile for user:', user.id);
			const accessToken = localStorage.getItem('access_token');

			if (!accessToken) {
				console.error('[UpdateProfilePage] No access token found');
				navigate('/login');
				return;
			}

			try {
				const res = await fetchWithRefresh(
					`${API_BASE_URL}/accounts/profiles/${user.id}/`,
					accessToken,
					{ method: 'GET' }
				);

				if (!res) {
					console.error('[UpdateProfilePage] Token refresh failed');
					navigate('/login');
					return;
				}

				if (res.ok) {
					const data = await res.json();
					console.log('[UpdateProfilePage] Profile data retrieved:', data);
					setForm({
						bio: data.bio || '',
						favorite_anime: data.favorite_anime || '',
						favorite_meal: data.favorite_meal || '',
						location: data.location || '',
						personal_website: data.personal_website || '',
						dietary_preferences: data.dietary_preferences || '',
					});
					setAvatarPreview(user.avatarUrl || null);
				} else {
					const message = await parseDjangoError(res);
					console.error('[UpdateProfilePage] Failed to fetch profile:', message);
					// Profile might not exist yet, that's okay
					setAvatarPreview(user.avatarUrl || null);
				}
			} catch (err) {
				console.error('[UpdateProfilePage] Error fetching profile:', err);
				setError('Error loading profile');
				setErrorMessage(err instanceof Error ? err.message : String(err));
				setShowErrorModal(true);
			} finally {
				setProfileLoading(false);
			}
		};

		fetchProfile();
	}, [user, navigate]);

	const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		setForm({
			...form,
			[e.target.name]: e.target.value
		});
	};

	const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (e.target.files && e.target.files[0]) {
			const file = e.target.files[0];
			setAvatar(file);
			setAvatarPreview(URL.createObjectURL(file));
			console.log('[UpdateProfilePage] Avatar selected:', file.name);
		}
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();

		if (!user) {
			console.error('[UpdateProfilePage] No user found on submit');
			navigate('/login');
			return;
		}

		setError('');
		setErrorMessage('');
		setIsLoading(true);

		const accessToken = localStorage.getItem('access_token');
		if (!accessToken) {
			console.error('[UpdateProfilePage] No access token found');
			navigate('/login');
			return;
		}

		try {
			console.log('[UpdateProfilePage] Updating profile...');

			// Build FormData
			const formData = new FormData();
			Object.entries(form).forEach(([key, value]) => {
				formData.append(key, value);
			});

			if (avatar) {
				formData.append('avatar', avatar);
				console.log('[UpdateProfilePage] Including avatar in update');
			}

			// Make request with auto token refresh
			const res = await fetchWithRefresh(
				`${API_BASE_URL}/accounts/profiles/${user.id}/`,
				accessToken,
				{
					method: 'PUT',
					body: formData,
				}
			);

			if (!res) {
				console.error('[UpdateProfilePage] Token refresh failed during update');
				navigate('/login');
				return;
			}

			if (res.ok) {
				const data = await res.json();
				console.log('[UpdateProfilePage] Profile updated successfully:', data);

				// Update user avatar in auth context if changed
				if (avatar && data.avatar) {
					setUser({
						...user,
						avatarUrl: data.avatar
					});
				}

				// Navigate to home or recipes page
				console.log('[UpdateProfilePage] Navigating to home page');
				navigate('/');
			} else {
				const message = await parseDjangoError(res);
				console.error('[UpdateProfilePage] Profile update failed:', message);
				setError('Profile update failed');
				setErrorMessage(message);
				setShowErrorModal(true);
			}
		} catch (err) {
			console.error('[UpdateProfilePage] Error updating profile:', err);
			setError('Network error while updating profile');
			setErrorMessage(err instanceof Error ? err.message : String(err));
			setShowErrorModal(true);
		} finally {
			setIsLoading(false);
		}
	};

	// Show loading state while auth is initializing
	if (isLoading || profileLoading) {
		return (
			<div className="update-profile-page">
				<div className="update-profile-form">
					<h1 className="update-profile-form__heading">Loading...</h1>
					<p className="update-profile-form__subtitle">
						Preparing your profile
					</p>
				</div>
			</div>
		);
	}

	// Don't render form if no user (will redirect)
	if (!user) {
		return null;
	}

	return (
		<>
			<PopUpModal
				isOpen={showErrorModal}
				onClose={() => setShowErrorModal(false)}
			>
				<div>
					{error}
					<br/>
					{errorMessage.split('\n').map((line, idx) => (
						<React.Fragment key={idx}>
							{line}
							<br/>
						</React.Fragment>
					))}
				</div>
			</PopUpModal>
			<div className="update-profile-page">
				<div className="update-profile-form">
					<h1 className="update-profile-form__heading">
						Power Up Your Profile
					</h1>
					<p className="update-profile-form__subtitle">
						Tell the community about your anime food journey
					</p>
					<form
						className="update-profile-form__form"
						onSubmit={handleSubmit}
					>
						<div className="update-profile-form__field">
							<label
								htmlFor="avatar"
								className="update-profile-form__label"
							>
								Avatar
							</label>
							<input
								id="avatar"
								name="avatar"
								type="file"
								accept="image/*"
								onChange={handleAvatarChange}
								className="update-profile-form__input"
								disabled={isLoading}
							/>
							{avatarPreview && (
								<div className="update-profile-form__avatar-preview">
									<img
										src={avatarPreview}
										alt="Avatar Preview"
										style={{ maxWidth: '120px', borderRadius: '50%' }}
									/>
								</div>
							)}
						</div>
						<div className="update-profile-form__field">
							<label
								htmlFor="bio"
								className="update-profile-form__label"
							>
								Bio
							</label>
							<textarea
								id="bio"
								name="bio"
								value={form.bio}
								onChange={handleChange}
								placeholder="Tell your story... Are you a cooking ninja or a ramen master?"
								className="update-profile-form__textarea"
								rows={4}
								maxLength={300}
								disabled={isLoading}
							/>
							<div
								className="update-profile-form__char-counter"
								style={{
									textAlign: 'right',
									fontSize: '0.9em',
									color: form.bio.length >= 300 ? 'red' : '#666'
								}}
							>
								{form.bio.length}/300 characters
							</div>
						</div>
						<div className="update-profile-form__field">
							<label
								htmlFor="favorite_anime"
								className="update-profile-form__label"
							>
								Favorite Anime
							</label>
							<input
								id="favorite_anime"
								name="favorite_anime"
								value={form.favorite_anime}
								onChange={handleChange}
								placeholder="e.g., Food Wars!, One Piece, Naruto"
								className="update-profile-form__input"
								disabled={isLoading}
							/>
						</div>
						<div className="update-profile-form__field">
							<label
								htmlFor="favorite_meal"
								className="update-profile-form__label"
							>
								Favorite Anime Meal
							</label>
							<input
								id="favorite_meal"
								name="favorite_meal"
								value={form.favorite_meal}
								onChange={handleChange}
								placeholder="e.g., Ichiraku Ramen, Senzu Beans, Meat on the Bone"
								className="update-profile-form__input"
								disabled={isLoading}
							/>
						</div>
						<div className="update-profile-form__field">
							<label
								htmlFor="location"
								className="update-profile-form__label"
							>
								Location
							</label>
							<input
								id="location"
								name="location"
								value={form.location}
								onChange={handleChange}
								placeholder="e.g., Hidden Leaf Village, Tokyo, Flavor Town"
								className="update-profile-form__input"
								disabled={isLoading}
							/>
						</div>
						<div className="update-profile-form__field">
							<label
								htmlFor="personal_website"
								className="update-profile-form__label"
							>
								Personal Website
							</label>
							<input
								id="personal_website"
								name="personal_website"
								value={form.personal_website}
								onChange={handleChange}
								placeholder="https://your-awesome-site.com"
								type="url"
								className="update-profile-form__input"
								disabled={isLoading}
							/>
						</div>
						<div className="update-profile-form__field">
							<label
								htmlFor="dietary_preferences"
								className="update-profile-form__label"
							>
								Dietary Preferences
							</label>
							<textarea
								id="dietary_preferences"
								name="dietary_preferences"
								value={form.dietary_preferences}
								onChange={handleChange}
								placeholder="Any dietary restrictions or preferences? (e.g., vegetarian, gluten-free, spicy food lover)"
								className="update-profile-form__textarea"
								rows={3}
								disabled={isLoading}
							/>
						</div>
						<button
							type="submit"
							className="update-profile-form__button"
							disabled={isLoading}
						>
							{isLoading ? 'Updating Profile...' : 'Update Profile'}
						</button>
					</form>
					<div className="update-profile-form__footer">
						Want to explore first?{' '}
						<a href="/" className="update-profile-form__link">
							Skip to home
						</a>
					</div>
				</div>
			</div>
		</>
	);
};

export default UpdateProfilePage;
