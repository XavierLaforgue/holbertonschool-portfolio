import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css';
import logo from '../assets/logo.png';
import { useAuth } from '../context/useAuth'; 


const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = React.useState(false);
  const menuRef = React.useRef<HTMLLIElement>(null);

  const handleMenuToggle = () => {
    console.log('[Header] Toggle menu:', !menuOpen);
    setMenuOpen((open) => !open);
  };

  const handleLogout = () => {
    console.log('[Header] Logging out');
    logout();
    setMenuOpen(false);
  };

  // Close menu when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    };

    if (menuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [menuOpen]);

  return (
    <header className={`header`}>
      <Link to="/" className="header__logo">
        <img src={logo} alt="Animize Eat Logo" />
        <span className="header__title">Animize Eat</span>
      </Link>
      <nav className="header__nav">
        <ul>
          {/* Show login, sign-up, and about if not logged in */}
          {!user && (
            <>
              <li key="login" id="header__nav__first">
                <Link 
                  to="/login"
                  title="Login"
                >Login</Link>
              </li>
              <li key="signup">
                <Link 
                  to="/signup"
                  title="Sign-up"
                >Sign-up</Link>
              </li>
              <li key="about" id='header__nav__last'>
                <Link 
                  to="/about"
                  title="About"
                >About</Link>
              </li>
            </>
          )}
          {/* Show username and avatar with dropdown if logged in */}
          {user && (
            <>
              <li key="recipes" id="header__nav__first">
                <Link 
                  to="/Recipes"
                  title="Recipes"
                >Recipes</Link>
              </li>
              <li key="user" id="header__nav__last" className="header__user-dropdown" ref={menuRef}>
                <button
                  className="header__user-btn"
                  aria-haspopup="true"
                  aria-expanded={menuOpen}
                  onClick={handleMenuToggle}
                  type="button"
                >
                  {user.avatarUrl ? (
                    <img
                      src={user.avatarUrl}
                      alt={`${user.username}'s avatar`}
                      className="header__avatar"
                      onError={(e) => {
                        console.error('[Header] Failed to load avatar:', user.avatarUrl);
                        e.currentTarget.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="header__avatar-placeholder">
                      {user.username.charAt(0).toUpperCase()}
                    </div>
                  )}
                  <span className="header__user-name">{user.username}</span>
                  <span className="header__user-caret">{menuOpen ? '▲' : '▼'}</span>
                </button>
                {menuOpen && (
                  <ul className="header__user-menu">
                    <li><Link to="/account" onClick={() => setMenuOpen(false)}>Account</Link></li>
                    <li><Link to="/profile" onClick={() => setMenuOpen(false)}>Profile</Link></li>
                    <li><Link to="/liked" onClick={() => setMenuOpen(false)}>Liked recipes</Link></li>
                    <li><Link to="/saved" onClick={() => setMenuOpen(false)}>Saved recipes</Link></li>
                    <li><Link to="/about" onClick={() => setMenuOpen(false)}>About Animize Eat</Link></li>
                    <li><button className="header__user-logout" onClick={handleLogout}>Log out</button></li>
                  </ul>
                )}
              </li>
            </>
          )}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
