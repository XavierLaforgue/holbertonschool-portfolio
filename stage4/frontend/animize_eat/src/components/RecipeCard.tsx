import React from 'react';
import '../styles/RecipeCard.css';

interface User {
  name: string;
  avatar: string;
}

interface Recipe {
  id: number;
  image: string;
  title: string;
  description: string;
  user: User;
}

interface RecipeCardProps {
  recipe: Recipe;
}

const RecipeCard: React.FC<RecipeCardProps> = ({ recipe }) => {
  return (
    <div className="recipe-card">
      <img className="recipe-card__image" src={recipe.image} alt={recipe.title} />
      <div className="recipe-card__content">
        <h3 className="recipe-card__title">{recipe.title}</h3>
        <p className="recipe-card__desc">{recipe.description}</p>
        <div className="recipe-card__user">
          <img className="recipe-card__avatar" src={recipe.user.avatar} alt={recipe.user.name} />
          <span className="recipe-card__username">{recipe.user.name}</span>
        </div>
      </div>
    </div>
  );
};

export default RecipeCard;
