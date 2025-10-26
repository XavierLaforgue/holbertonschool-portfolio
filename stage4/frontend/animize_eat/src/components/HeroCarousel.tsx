import React from 'react';
import '../styles/HeroCarousel.css';
import RecipeCard from './RecipeCard';

// Dummy data for demonstration
const recipes = [
  {
    id: 1,
    image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836',
    title: 'Ramen of the Fire Nation',
    description: 'Spicy pork ramen inspired by Avatar: The Last Airbender.',
    user: {
      name: 'Azula',
      avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
    }
  },
  {
    id: 2,
    image: 'https://images.unsplash.com/photo-1464306076886-debede1a7c94',
    title: 'Sailor Moon Bento',
    description: 'Cute bento box with magical girl flair.',
    user: {
      name: 'Usagi',
      avatar: 'https://randomuser.me/api/portraits/women/65.jpg'
    }
  },
  {
    id: 3,
    image: 'https://images.unsplash.com/photo-1519864600265-abb23847ef2c',
    title: 'Naruto’s Ichiraku Ramen',
    description: 'Classic shoyu ramen with narutomaki.',
    user: {
      name: 'Naruto',
      avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
    }
  }
];

const HeroCarousel: React.FC = () => {
  // Duplicate recipes for seamless infinite scroll
  const duplicatedRecipes = [...recipes, ...recipes];

  return (
    <section className="recipe-carousel">
      <h1>Bring your favorite animes to your kitchen and your table</h1>
      <div className="recipe-carousel__slider">
        {duplicatedRecipes.map((recipe, index) => (
          <RecipeCard key={`${recipe.id}-${index}`} recipe={recipe} />
        ))}
      </div>
    </section>
  );
};

export default HeroCarousel;
