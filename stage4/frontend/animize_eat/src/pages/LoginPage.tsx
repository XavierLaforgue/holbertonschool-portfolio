import React, { useState } from 'react';
import { API_BASE_URL } from '../config';
import PopUpModal from '../components/PopUpModal';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPage.css';
import parseDjangoError from '../parseDjangoError';
import { useAuth } from '../context/useAuth';


const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      console.log('[LoginPage] Attempting login...');

      // Get tokens
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
        setError('Login failed');
        setErrorMessage(message);
        setShowErrorModal(true);
        setIsLoading(false);
        return;
      }

      const tokenPayload = await tokenRes.json();
      const accessToken = tokenPayload.access;
      const refreshToken = tokenPayload.refresh;

      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('refresh_token', refreshToken);
      console.log('[LoginPage] Tokens stored successfully');

      // Get user info
      const userRes = await fetch(`${API_BASE_URL}/accounts/me/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });

      if (!userRes.ok) {
        const message = await parseDjangoError(userRes);
        setError('Failed to fetch user info');
        setErrorMessage(message);
        setShowErrorModal(true);
        setIsLoading(false);
        return;
      }

      const userInfo = await userRes.json();
      console.log('[LoginPage] User info retrieved:', userInfo.username);

      // Update auth context
      login({
        id: userInfo.id,
        username: userInfo.username,
        avatarUrl: userInfo.avatar || ''
      });

      console.log('[LoginPage] Login successful, redirecting...');
      navigate('/');

    } catch (err) {
      console.error('[LoginPage] Login error:', err);
      setError('Network error while trying to log in');
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
        onClose={() => setShowErrorModal(false)}
      >
        <div>
          {error}
          <br />
          {errorMessage.split('\n').map((line, idx) => (
            <React.Fragment key={idx}>
              {line}
              <br />
            </React.Fragment>
          ))}
        </div>
      </PopUpModal>
      <div className="login-page">
        <div className="login-form">
          <h1 className="login-form__heading">Welcome Back</h1>
          <p className="login-form__subtitle">
            Log in to continue your culinary adventure
          </p>
          <form className="login-form__form" onSubmit={handleSubmit}>
            <div className="login-form__field">
              <label htmlFor="username" className="login-form__label">
                Username
              </label>
              <input
                id="username"
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder="Enter your username"
                className="login-form__input"
                required
                disabled={isLoading}
              />
            </div>
            <div className="login-form__field">
              <label htmlFor="password" className="login-form__label">
                Password
              </label>
              <input
                id="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                placeholder="Enter your password"
                type="password"
                className="login-form__input"
                required
                disabled={isLoading}
              />
            </div>
            <button
              type="submit"
              className="login-form__button"
              disabled={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Log In'}
            </button>
          </form>
          <div className="login-form__footer">
            Don't have an account?{' '}
            <a href="/signup" className="login-form__link">
              Sign up here
            </a>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginPage;
