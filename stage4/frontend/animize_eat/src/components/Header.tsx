import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css';
import logo from '../assets/logo.png';
import { useAuth } from '../context/useAuth'; 


const Header: React.FC = () => {
  const { user } = useAuth();

  const navItems = [
    { key: 'login', label: 'Login', linkto: '/login' },
    { key: 'signup', label: 'Sign-up', linkto: '/signup' },
    { key: 'about', label: 'About', linkto: '/about' },
  ];

  return (
    <header className={`header`}>
      <Link to="/" className="header__logo">
        <img src={logo} alt="Animize Eat Logo" />
        <span className="header__title">Animize Eat</span>
      </Link>
      <nav className="header__nav">
        <ul>
          {/* Show login and sign-up if not logged in */}
          {/* {!user && (
            <>
              <li key="login">
                <Link to="/login" title="Login" id="header__nav__first">Login</Link>
              </li>
              <li key="signup">
                <Link to="/signup" title="Sign-up">Sign-up</Link>
              </li>
            </>
          )} */}
          {/* Show username and avatar if logged in */}
          {/* {user && (
            <li key="user" id="header__nav__first">
              <button className="header__user-btn">
                {user.avatarUrl && (
                  <img src={user.avatarUrl} alt="avatar" className="header__avatar" />
                )}
                <span>{user.username}</span>
              </button>
            </li>
          )} */}
          {/* Always show About */}
          {navItems.map((item, idx) => {
            const isFirst = idx === 0;
            const isLast = idx === navItems.length - 1;
            let linkId = '';
            if (isFirst) linkId = 'header__nav__first';
            else if (isLast) linkId = 'header__nav__last';
            return (
              <li key={item.key}>
                <Link 
                  to={item.linkto}
                  title={item.label}
                  id={linkId}>
                   {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
