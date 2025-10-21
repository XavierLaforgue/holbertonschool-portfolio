import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css';
import logo from '../assets/logo.png';
import { useAuth } from '../context/useAuth'; 


const Header: React.FC = () => {
  const { user } = useAuth();
  const [menuOpen, setMenuOpen] = React.useState(false);
  const handleMenuToggle = () => setMenuOpen((open) => !open);
  const handleMenuClose = () => setMenuOpen(false);

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
              <li key="user" id="header__nav__last">
                <button
                  className="header__user-btn"
                  aria-haspopup="true"
                  aria-expanded={menuOpen}
                  onClick={handleMenuToggle}
                  onBlur={handleMenuClose}
                  type="button"
                >
                  {user.avatarUrl && (
                    <img 
                      src={user.avatarUrl} alt="avatar"
                      className="header__avatar" />
                  )}
                  <span className="header__user-name">{user.username}</span>
                  {/* <svg className="header__user-caret" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6L8 10L12 6" stroke="#333" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg> */} {/* build the inverted triangle */}
                  <span className="header__user-caret">▼</span> {/* use unicode character for the inverted triangle */}
                </button>
                {menuOpen && (
                  <ul className="header__user-menu">
                    <li><Link to="/account" onClick={handleMenuClose}>Account</Link></li>
                    <li><Link to="/profile" onClick={handleMenuClose}>Profile</Link></li>
                    <li><Link to="/liked" onClick={handleMenuClose}>Liked recipes</Link></li>
                    <li><Link to="/saved" onClick={handleMenuClose}>Saved recipes</Link></li>
                    <li><Link to="/about" onClick={handleMenuClose}>About Animize Eat</Link></li>
                    <li><button className="header__user-logout" onClick={() => { /* TODO: implement logout */ handleMenuClose(); }}>Log out</button></li>
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
