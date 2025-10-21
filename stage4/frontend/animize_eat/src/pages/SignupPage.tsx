import React, { useState, useContext } from 'react';
import { API_BASE_URL } from '../config';
import PopUpModal from '../components/PopUpModal';
import { useNavigate } from 'react-router-dom';
import '../styles/SignupPage.css';
import parseDjangoError from '../parseDjangoError';
import { AuthContext } from '../context/AuthContext';


const SignupForm: React.FC = () => {
	const auth = useContext(AuthContext);
	if (!auth) {
    	throw new Error('SignupForm must be used within an AuthProvider');
  	}
  	const { login } = auth;
	const [form, setForm] = useState(
		{ username: '', email: '', password: '' }
	);
	const [error, setError] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [success, setSuccess] = useState('');
	const [showErrorModal, setShowErrorModal] = useState(false);
	const navigate = useNavigate();

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setForm({ ...form, // copies all previous form values
			[e.target.name]: e.target.value // evaluate e.target.name to use it as the key to which the value e.target.value will be assigned
		});
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault(); // prevents the browser from reloading the page (which is its default behavior)
		setError('');
		setSuccess('');
		try {
			const res = await fetch(`${API_BASE_URL}/accounts/users/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(form),
			});
			if (res.ok) {
				setSuccess('Sign-up successful!');
				try {
					const res2 = await fetch(`${API_BASE_URL}/tokens/`, {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify(
							{username: form.username, password: form.password}
						),
						credentials: 'include',
					})
					if (res2.ok) {
						const payload = await res2.json();
						login({ id: payload.id, username: form.username });
						navigate('/profile/update',
							{ state: { success: success } }
						);
					} else {
						const message2 = await parseDjangoError(res2);
						setError('Login failed');
						setErrorMessage(message2);
						setShowErrorModal(true);
					}
				} catch (err) {
					setError('Network error while trying to log-in');
					setErrorMessage(err instanceof Error ? err.message : String(err));
					setShowErrorModal(true);
				}
			} else {
				const message = await parseDjangoError(res);
				setError('Sign-up failed');
				setErrorMessage(message);
				setShowErrorModal(true);
			}
		} catch (err) {
			setError('Network error while trying to sign-up');
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
			      />
			    </div>
			    <button type="submit" className="signup-form__button">
			      Sign Up
			    </button>
			  </form>
			  <div className="signup-form__footer">
			    Already have an account?{' '}
			    <a href="/login" className="signup-form__link">
			      Log in here
			    </a>
			  </div>
			</div>
		  </div>
		</>
	);
};

export default SignupForm;
