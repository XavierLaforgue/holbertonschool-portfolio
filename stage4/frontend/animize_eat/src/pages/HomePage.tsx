import React from 'react';
import HeroCarousel from '../components/HeroCarousel';
import SiteManual from '../components/SiteManual';


const HomePage: React.FC = () => {
	return (
		<main className="main-content">
            <HeroCarousel />
            <SiteManual />
        </main>
	)
}

export default HomePage;
