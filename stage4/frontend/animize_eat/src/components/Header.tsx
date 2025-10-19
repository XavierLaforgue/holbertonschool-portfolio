import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css';
import logo from '../assets/logo.png';


const Header: React.FC = () => {
  const navItems = [
    { key: 'login', label: 'Login', linkto: '/login' },
    { key: 'signup', label: 'Sign-up', linkto: '/signup' },
    { key: 'about', label: 'About', linkto: '/about' }
  ];

  return (
    <header className={`header`}>
      <Link to="/" className="header__logo">
        <img src={logo} alt="Animize Eat Logo" />
        <span className="header__title">Animize Eat</span>
      </Link>
      <nav className="header__nav">
        <ul>
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
