import React, { useContext, useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';
import PopUpModal from '../components/PopUpModal';
import { useNavigate } from 'react-router-dom';
import '../styles/UpdateProfilePage.css';
import parseDjangoError from '../parseDjangoError';
import { AuthContext } from '../context/AuthContext';


const UpdateProfilePage: React.FC = () => {
	const auth = useContext(AuthContext);
	if (!auth) {
		throw new Error(`UpdateProfilePage must be used within an AuthProvider`);
	} else if (!auth.user) {
		throw new Error(`UpdateProfilePage should be accessible only after being logged-in`)
	}
	const userId = auth.user.id;
	const [form, setForm] = useState({ // TODO: add missing fields to the profile model in the backend
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
	const [success, setSuccess] = useState('');
	const [showErrorModal, setShowErrorModal] = useState(false);
	const navigate = useNavigate();

	useEffect(() => {
		async function fetchProfile() { // TODO: create and add fetchRefresh function to refresh access tokens if a fetch request with tokens is rejected du to invalid/expired token
			try {
				const res = await fetch(`${API_BASE_URL}/accounts/profiles/${userId}/`, { // TODO: change endpoint so the required id would be the userId and not the profile id
					method: 'GET',
					credentials: 'include',
				});
				if (res.ok) {
					const data = await res.json();
					setForm({
						bio: data.bio || '',
						favorite_anime: data.favorite_anime || '',
						favorite_meal: data.favorite_meal || '',
						location: data.location || '',
						personal_website: data.personal_website || '',
						dietary_preferences: data.dietary_preferences || '',
					});
				    if (data.avatar) { // TODO: configure django server so it will serve the avatar from a url while stored in its local storage
						setAvatarPreview(data.avatar);
          			}
        		}
    		} catch (err) {
				setError('Network error while trying to retrieve user profile');
				setErrorMessage(err instanceof Error ? err.message : String(err));
				setShowErrorModal(true);
			}
		}
		fetchProfile();
	}, [userId]);

	const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		setForm({ ...form,
			[e.target.name]: e.target.value
		});
	};

	const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (e.target.files && e.target.files[0]) {
			setAvatar(e.target.files[0]);
			setAvatarPreview(URL.createObjectURL(e.target.files[0]));
		}
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError('');
		setSuccess('');
		try {
			const formData = new FormData();
			Object.entries(form).forEach(([key, value]) => {
				formData.append(key, value);
			});
			if (avatar) {
				formData.append('avatar', avatar);
			}
			const res = await fetch(`${API_BASE_URL}/accounts/profiles/${userId}/`,
				{
					method: 'PUT',
					body: formData, // TODO: configure Django so it can receive the upload of an image
					credentials: 'include',
				}
			);
			if (res.ok) {
				setSuccess('Profile update successful!');
				navigate('/recipes', { state: { success: success } });
			} else {
				const message = await parseDjangoError(res);
				setError('Profile update failed');
				setErrorMessage(message);
				setShowErrorModal(true);
			}
		} catch (err) {
			setError('Network error while trying to update profile');
			setErrorMessage(err instanceof Error ? err.message : String(err));
			setShowErrorModal(true);
		}
	};

	return (
		<>
		  <PopUpModal
		    isOpen={showErrorModal}
			onClose={() => setShowErrorModal(false)}>
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
				Power Up Your Profile</h1>
			  <p className="update-profile-form__subtitle">
				Tell the community about your anime food journey
			  </p>
			  <form 
			    className="update-profile-form__form"
				onSubmit={handleSubmit}>
			      <div className="update-profile-form__field">
				    <label 
					  htmlFor="avatar"
					  className="update-profile-form__label">
						Avatar
					</label>
					<input
					  id="avatar"
					  name="avatar"
					  type="file"
					  accept="image/*"
					  onChange={handleAvatarChange}
					  className="update-profile-form__input"
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
					    htmlFor="bio" className="update-profile-form__label">
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
					  />
					  <div 
					    className="update-profile-form__char-counter"
						style={{ 
						  textAlign: 'right', 
						  fontSize: '0.9em', 
						  color: form.bio.length >= 300 ? 'red' : '#666'
						}}>
						{form.bio.length}/300 characters
					  </div>
					</div>
				  <div className="update-profile-form__field">
					<label htmlFor="favorite_anime"
					  className="update-profile-form__label">
						Favorite Anime
					</label>
					<input
					  id="favorite_anime"
					  name="favorite_anime"
					  value={form.favorite_anime}
					  onChange={handleChange}
					  placeholder="e.g., Food Wars!, One Piece, Naruto"
					  className="update-profile-form__input"
					/>
				  </div>
				  <div className="update-profile-form__field">
					<label htmlFor="favorite_meal"
					  className="update-profile-form__label">
						Favorite Anime Meal
					</label>
					<input
					  id="favorite_meal"
					  name="favorite_meal"
					  value={form.favorite_meal}
					  onChange={handleChange}
					  placeholder="e.g., Ichiraku Ramen, Senzu Beans, Meat on the Bone"
					  className="update-profile-form__input"
					/>
				  </div>
				  <div className="update-profile-form__field">
					<label htmlFor="location" 
					  className="update-profile-form__label">
						Location
					</label>
					<input
					  id="location"
					  name="location"
					  value={form.location}
					  onChange={handleChange}
					  placeholder="e.g., Hidden Leaf Village, Tokyo, Flavor Town"
					  className="update-profile-form__input"
					/>
				  </div>
				  <div className="update-profile-form__field">
					<label htmlFor="personal_website" 
					  className="update-profile-form__label">
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
					/>
				  </div>
				  <div className="update-profile-form__field">
				    <label htmlFor="dietary_preferences" 
					  className="update-profile-form__label">
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
					/>
				  </div>
				  <button type="submit" className="update-profile-form__button">
					Update Profile
				  </button>
			  </form>
			<div className="update-profile-form__footer">
			  Want to explore first?{' '}
			  <a href="/recipes" className="update-profile-form__link">
			  	Skip to recipes
			  </a>
			</div>
		  </div>
		</div>
	  </>
	);
};

export default UpdateProfilePage;
