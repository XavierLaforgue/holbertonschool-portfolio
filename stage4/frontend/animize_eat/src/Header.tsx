// import React, { useState, useEffect } from 'react';
import React from 'react';
import './Header.css';
import logo from './assets/logo.png';

const Header: React.FC = () => {
  // const [scrolled, setScrolled] = useState(false);

  // useEffect(() => {
  //   const handleScroll = () => {
  //     setScrolled(window.scrollY > 20);
  //   };

  //   window.addEventListener('scroll', handleScroll);
  //   return () => window.removeEventListener('scroll', handleScroll);
  // }, []);

  const navItems = [
    { href: '#login', label: 'Login' },
    { href: '#signup', label: 'Sign-up' },
    { href: '#about', label: 'About' }
  ];

  return (
    // <header className={`header ${scrolled ? 'header--scrolled' : ''}`}>
    <header className={`header`}>
      <a href="/" className="header__logo">
        <img src={logo} alt="Animize Eat Logo" />
        <span className="header__title">Animize Eat</span>
      </a>
      <nav className="header__nav">
        {navItems.map((item, idx) => {
          const isFirst = idx === 0;
          const isLast = idx === navItems.length - 1;
          let linkId = '';
          if (isFirst) linkId = 'header__nav__first';
          else if (isLast) linkId = 'header__nav__last';
          return (
            <a
              key={item.href}
              href={item.href}
              title={item.label}
              id={linkId}
            >
              {item.label}
            </a>
          );
        })}
      </nav>
    </header>
  );
};

export default Header;
