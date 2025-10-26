import React, { useState } from 'react';
import { API_BASE_URL } from '../config';
import PopUpModal from '../components/PopUpModal';
import { useNavigate, Link } from 'react-router-dom';
import '../styles/SignupPage.css';
import parseDjangoError from '../parseDjangoError';
import { useAuth } from '../context/useAuth';


const SignupPage: React.FC = () => {
	const { login } = useAuth();
	const [form, setForm] = useState({ username: '', email: '', password: '' });
	const [error, setError] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [showErrorModal, setShowErrorModal] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setForm({ ...form, // copies all previous form values
			[e.target.name]: e.target.value // evaluate e.target.name to use it as the key to which the value e.target.value will be assigned
		});
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError('');
		setErrorMessage('');
		setIsLoading(true);

		try {
			// Step 1: Create user account
			console.log('[SignupPage] Step 1: Creating user account...');
			const createUserRes = await fetch(`${API_BASE_URL}/accounts/users/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(form),
			});

			if (!createUserRes.ok) {
				const message = await parseDjangoError(createUserRes);
				console.error('[SignupPage] User creation failed:', message);
				setError('Sign-up failed');
				setErrorMessage(message);
				setShowErrorModal(true);
				setIsLoading(false);
				return;
			}

			const userData = await createUserRes.json();
			const userId = userData.id;
			console.log('[SignupPage] User created successfully:', userId);

			// Step 2: Get authentication tokens
			console.log('[SignupPage] Step 2: Getting authentication tokens...');
			const tokenRes = await fetch(`${API_BASE_URL}/tokens/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					username: form.username,
					password: form.password
				}),
			});

			if (!tokenRes.ok) {
				const message = await parseDjangoError(tokenRes);
				console.error('[SignupPage] Token generation failed:', message);
				setError('Auto-login failed after signup');
				setErrorMessage(message);
				setShowErrorModal(true);
				setIsLoading(false);
				return;
			}

			const tokenData = await tokenRes.json();
			const accessToken = tokenData.access;
			const refreshToken = tokenData.refresh;

			localStorage.setItem('access_token', accessToken);
			localStorage.setItem('refresh_token', refreshToken);
			console.log('[SignupPage] Tokens stored successfully');

			// Step 3: Get user info including avatar
			console.log('[SignupPage] Step 3: Fetching user info...');
			const userInfoRes = await fetch(`${API_BASE_URL}/accounts/me/`, {
				method: 'GET',
				headers: {
					'Authorization': `Bearer ${accessToken}`,
				},
			});

			if (!userInfoRes.ok) {
				const message = await parseDjangoError(userInfoRes);
				console.error('[SignupPage] User info fetch failed:', message);
				// Still log them in with basic info
				login({
					id: userId,
					username: form.username,
					avatarUrl: ''
				});
				console.log('[SignupPage] Logged in with basic info, navigating to profile update');
				navigate('/profile/update');
				setIsLoading(false);
				return;
			}

			const userInfo = await userInfoRes.json();
			console.log('[SignupPage] User info retrieved:', userInfo);

			// Step 4: Update auth context and navigate
			login({
				id: userId,
				username: form.username,
				avatarUrl: userInfo.avatar || ''
			});

			console.log('[SignupPage] Signup complete! Navigating to profile update...');
			navigate('/profile/update');

		} catch (err) {
			console.error('[SignupPage] Unexpected error during signup:', err);
			setError('Network error during sign-up');
			setErrorMessage(err instanceof Error ? err.message : String(err));
			setShowErrorModal(true);
		} finally {
			setIsLoading(false);
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
		  <div className="signup-page">
		    <div className="signup-form">
			  <h1 className="signup-form__heading">Join the Adventure</h1>
			  <p className="signup-form__subtitle">
			    Create your account and start exploring anime-inspired recipes
			  </p>
			  <form className="signup-form__form" onSubmit={handleSubmit}>
			    <div className="signup-form__field">
			      <label htmlFor="username" className="signup-form__label">
			        Username
			      </label>
			      <input
				    id="username"
			        name="username"
			        value={form.username}
			        onChange={handleChange}
			        placeholder="Choose your hero name"
			        className="signup-form__input"
			        required
			        disabled={isLoading}
			      />
			    </div>
			    <div className="signup-form__field">
			      <label htmlFor="email" className="signup-form__label">
			        Email
			      </label>
			      <input
				    id="email"
			        name="email"
			        value={form.email}
			        onChange={handleChange}
			        placeholder="your.email@example.com"
			        type="email"
			        className="signup-form__input"
			        required
			        disabled={isLoading}
			      />
			    </div>
			    <div className="signup-form__field">
			      <label htmlFor="password" className="signup-form__label">
			        Password
			      </label>
			      <input
				    id="password"
			        name="password"
			        value={form.password}
			        onChange={handleChange}
			        placeholder="Create a strong password"
			        type="password"
			        className="signup-form__input"
			        required
			        disabled={isLoading}
			      />
			    </div>
			    <button type="submit" className="signup-form__button" disabled={isLoading}>
			      {isLoading ? 'Creating Account...' : 'Sign Up'}
			    </button>
			  </form>
			  <div className="signup-form__footer">
			    Already have an account?{' '}
			    <Link to="/login" className="signup-form__link">
			      Log in here
			    </Link>
			  </div>
			</div>
		  </div>
		</>
	);
};

export default SignupPage;
