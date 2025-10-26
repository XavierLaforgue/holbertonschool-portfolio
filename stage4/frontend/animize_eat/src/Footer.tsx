import React from 'react';
import './Footer.css';
import logo from './assets/logo.png';

interface LinkItem {
  href: string;
  label: string;
}

const Footer: React.FC = () => {
  const quickLinks: LinkItem[] = [
    { href: '/', label: 'Home' },
    { href: '#recipes', label: 'Recipes' },
    { href: '#about', label: 'About' },
    { href: '#contact', label: 'Contact' }
  ];

  const communityLinks: LinkItem[] = [
    { href: '#twitter', label: 'Twitter' },
    { href: '#instagram', label: 'Instagram' },
    { href: '#discord', label: 'Discord' },
    { href: '#github', label: 'GitHub' }
  ];

  const legalLinks: LinkItem[] = [
    { href: '#privacy', label: 'Privacy Policy' },
    { href: '#terms', label: 'Terms of Service' },
    { href: '#cookies', label: 'Cookie Policy' }
  ];

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer__container">
        {/* Brand Section */}
        <div className="footer__section footer__section--brand">
          <div className="footer__logo">
            <img src={logo} alt="Animize Eat Logo" />
            <span className="footer__brand-name">Animize Eat</span>
          </div>
          <p className="footer__tagline">
            Where anime passion meets culinary adventure
          </p>
          <p className="footer__description">
            Create and discover anime-inspired recipes that bring your favorite shows to life, one delicious bite at a time.
          </p>
        </div>

        {/* Quick Links */}
        <div className="footer__section">
          <h3 className="footer__section-title">Quick Links</h3>
          <ul className="footer__links">
            {quickLinks.map((link) => (
              <li key={link.href}>
                <a href={link.href} className="footer__link">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        {/* Community Links */}
        <div className="footer__section">
          <h3 className="footer__section-title">Community</h3>
          <ul className="footer__links">
            {communityLinks.map((link) => (
              <li key={link.href}>
                <a href={link.href} className="footer__link">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        {/* Legal Links */}
        <div className="footer__section">
          <h3 className="footer__section-title">Legal</h3>
          <ul className="footer__links">
            {legalLinks.map((link) => (
              <li key={link.href}>
                <a href={link.href} className="footer__link">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="footer__bottom">
        <div className="footer__bottom-content">
          <p className="footer__copyright">
            &copy; {currentYear} Animize Eat. All rights reserved.
          </p>
          <p className="footer__credits">
            Made with <span className="footer__heart">❤️</span> for anime and food lovers
          </p>
        </div>
        <button
          className="footer__back-to-top"
          onClick={scrollToTop}
          aria-label="Back to top"
          title="Back to top"
        >
          <span className="footer__arrow">↑</span>
        </button>
      </div>
    </footer>
  );
};

export default Footer;
