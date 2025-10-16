import React from 'react';
import './SiteManual.css';

const SiteManual: React.FC = () => {
  return (
    <section className="site-manual">
      <div className="site-manual__container">
        <h2 className="site-manual__title">How Animize Eat Works</h2>
        <p className="site-manual__subtitle">
          Where anime passion meets culinary adventure
        </p>

        <div className="site-manual__modes">
          {/* Experience Mode */}
          <div className="site-manual__mode site-manual__mode--experience">
            <div className="site-manual__mode-header">
              <h3 className="site-manual__mode-title">Experience Mode</h3>
              <span className="site-manual__mode-badge">Discover & Cook</span>
            </div>
            <div className="site-manual__mode-content">
              <div className="site-manual__step">
                <span className="site-manual__step-number">1</span>
                <div className="site-manual__step-content">
                  <h4>Think of Your Favorite Anime</h4>
                  <p>Got a show that makes you hungry? Let's bring those flavors to life</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">2</span>
                <div className="site-manual__step-content">
                  <h4>Search for the Perfect Match</h4>
                  <p>Browse meals that capture the vibe of your beloved series</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">3</span>
                <div className="site-manual__step-content">
                  <h4>Follow the Steps</h4>
                  <p>Clear instructions guide you through each delicious detail</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">4</span>
                <div className="site-manual__step-content">
                  <h4>Use Enhancement Tools</h4>
                  <p>Timers keep you on track (more tools coming soon)</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">5</span>
                <div className="site-manual__step-content">
                  <h4>Enjoy Your Anime-Fueled Culinary Event</h4>
                  <p>Savor every bite while living your anime dream</p>
                </div>
              </div>
            </div>
          </div>

          {/* Creator Mode */}
          <div className="site-manual__mode site-manual__mode--creator">
            <div className="site-manual__mode-header">
              <h3 className="site-manual__mode-title">Creator Mode</h3>
              <span className="site-manual__mode-badge">Build & Share</span>
            </div>
            <div className="site-manual__mode-content">
              <div className="site-manual__step">
                <span className="site-manual__step-number">✨</span>
                <div className="site-manual__step-content">
                  <h4>Go One Step Ahead</h4>
                  <p>Ready to create your own anime-inspired masterpiece?</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">🎨</span>
                <div className="site-manual__step-content">
                  <h4>Use Interactive Construction Tools</h4>
                  <p>Build your recipe with intuitive, powerful creation features</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">🍜</span>
                <div className="site-manual__step-content">
                  <h4>Craft Your Experience</h4>
                  <p>Design every aspect: ingredients, steps, timing, and anime inspiration</p>
                </div>
              </div>
              <div className="site-manual__step">
                <span className="site-manual__step-number">🌟</span>
                <div className="site-manual__step-content">
                  <h4>Share With the Community</h4>
                  <p>Publish your creation for others to enjoy—or keep it private, your choice</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="site-manual__cta">
          <p className="site-manual__cta-text">
            Your anime-inspired culinary journey begins now
          </p>
        </div>
      </div>
    </section>
  );
};

export default SiteManual;
