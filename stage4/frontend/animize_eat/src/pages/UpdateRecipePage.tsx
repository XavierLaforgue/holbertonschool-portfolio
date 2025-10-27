import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/UpdateRecipePage.css';
import { API_BASE_URL } from '../config';

interface Ingredient {
	id?: string;
	name: string;
	quantity: string;
	unit: string;
}

interface Recipe {
	id: string;
	title: string;
	cover_image?: string;
	ingredients?: Ingredient[];
}

const UpdateRecipePage: React.FC = () => {
	const { recipeId } = useParams<{ recipeId: string }>();
	const navigate = useNavigate();

	const [recipe, setRecipe] = useState<Recipe | null>(null);
	const [isLoading, setIsLoading] = useState(true);
	const [coverImage, setCoverImage] = useState<string | null>(null);
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [isUploadingImage, setIsUploadingImage] = useState(false);
	const fileInputRef = React.useRef<HTMLInputElement>(null);

	// Title editing
	const [title, setTitle] = useState('');
	const [isEditingTitle, setIsEditingTitle] = useState(false);
	const [isSavingTitle, setIsSavingTitle] = useState(false);

	// Ingredients
	const [ingredients, setIngredients] = useState<Ingredient[]>([]);
	const [newIngredient, setNewIngredient] = useState<Ingredient>({ name: '', quantity: '', unit: '' });
	const [isAddingIngredient, setIsAddingIngredient] = useState(false);
	const [isSavingIngredient, setIsSavingIngredient] = useState(false);

	// Fetch recipe data on mount
	useEffect(() => {
		const fetchRecipe = async () => {
			const accessToken = localStorage.getItem('access_token');

			if (!accessToken) {
				console.error('[UpdateRecipePage] No access token');
				navigate('/login');
				return;
			}

			try {
				console.log('[UpdateRecipePage] Fetching recipe:', recipeId);
				const response = await fetch(`${API_BASE_URL}/recipes/${recipeId}/`, {
					headers: {
						'Authorization': `Bearer ${accessToken}`,
					},
				});

				if (response.ok) {
					const data = await response.json();
					console.log('[UpdateRecipePage] Recipe loaded:', data);
					setRecipe(data);
					// Set title
					setTitle(data.title || 'Untitled Recipe');
					// Set cover image if it exists
					if (data.cover_image) {
						setCoverImage(data.cover_image);
					}
					// Set ingredients if they exist
					if (data.ingredients && Array.isArray(data.ingredients)) {
						setIngredients(data.ingredients);
					}
				} else {
					console.error('[UpdateRecipePage] Failed to fetch recipe:', response.status);
					alert('Failed to load recipe');
					navigate('/');
				}
			} catch (error) {
				console.error('[UpdateRecipePage] Error fetching recipe:', error);
				alert('Network error loading recipe');
				navigate('/');
			} finally {
				setIsLoading(false);
			}
		};

		if (recipeId) {
			fetchRecipe();
		}
	}, [recipeId, navigate]);

	const handleImageClick = () => {
		fileInputRef.current?.click();
	};

	const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (file) {
			// Validate file type
			if (!file.type.startsWith('image/')) {
				alert('Please select an image file');
				return;
			}

			// Validate file size (max 5MB)
			if (file.size > 5 * 1024 * 1024) {
				alert('Image size should be less than 5MB');
				return;
			}

			// Store the file for later upload
			setSelectedFile(file);

			// Create preview URL
			const reader = new FileReader();
			reader.onloadend = () => {
				setCoverImage(reader.result as string);
			};
			reader.readAsDataURL(file);
		}
	};

	const handleConfirmImage = async () => {
		if (!selectedFile || !recipeId) return;

		setIsUploadingImage(true);
		const accessToken = localStorage.getItem('access_token');

		if (!accessToken) {
			alert('Please log in to upload images');
			navigate('/login');
			return;
		}

		try {
			console.log('[UpdateRecipePage] Uploading cover image...');

			const formData = new FormData();
			formData.append('cover_image', selectedFile);

			const response = await fetch(`${API_BASE_URL}/recipes/${recipeId}/`, {
				method: 'PATCH',
				headers: {
					'Authorization': `Bearer ${accessToken}`,
				},
				body: formData,
			});

			if (response.ok) {
				const updatedRecipe = await response.json();
				console.log('[UpdateRecipePage] Image uploaded successfully');
				setRecipe(updatedRecipe);
				setSelectedFile(null); // Clear selected file after successful upload
				alert('Cover image updated!');
			} else {
				console.error('[UpdateRecipePage] Failed to upload image:', response.status);
				alert('Failed to upload image. Please try again.');
			}
		} catch (error) {
			console.error('[UpdateRecipePage] Error uploading image:', error);
			alert('Network error. Please try again.');
		} finally {
			setIsUploadingImage(false);
		}
	};

	const handleRemoveImage = () => {
		setCoverImage(null);
		setSelectedFile(null);
		if (fileInputRef.current) {
			fileInputRef.current.value = '';
		}
	};

	// Title handlers
	const handleTitleSave = async () => {
		if (!recipeId || !title.trim()) return;

		setIsSavingTitle(true);
		const accessToken = localStorage.getItem('access_token');

		if (!accessToken) {
			navigate('/login');
			return;
		}

		try {
			const response = await fetch(`${API_BASE_URL}/recipes/${recipeId}/`, {
				method: 'PATCH',
				headers: {
					'Authorization': `Bearer ${accessToken}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ title: title.trim() }),
			});

			if (response.ok) {
				const updatedRecipe = await response.json();
				setRecipe(updatedRecipe);
				setIsEditingTitle(false);
				console.log('[UpdateRecipePage] Title updated');
			} else {
				alert('Failed to update title');
			}
		} catch (error) {
			console.error('[UpdateRecipePage] Error updating title:', error);
			alert('Network error');
		} finally {
			setIsSavingTitle(false);
		}
	};

	// Ingredient handlers
	const handleAddIngredient = async () => {
		if (!recipeId || !newIngredient.name.trim() || !newIngredient.quantity.trim()) {
			alert('Please fill in ingredient name and quantity');
			return;
		}

		setIsSavingIngredient(true);
		const accessToken = localStorage.getItem('access_token');

		if (!accessToken) {
			navigate('/login');
			return;
		}

		try {
			const response = await fetch(`${API_BASE_URL}/recipes/${recipeId}/ingredients/`, {
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${accessToken}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(newIngredient),
			});

			if (response.ok) {
				const addedIngredient = await response.json();
				setIngredients([...ingredients, addedIngredient]);
				setNewIngredient({ name: '', quantity: '', unit: '' });
				setIsAddingIngredient(false);
				console.log('[UpdateRecipePage] Ingredient added');
			} else {
				alert('Failed to add ingredient');
			}
		} catch (error) {
			console.error('[UpdateRecipePage] Error adding ingredient:', error);
			alert('Network error');
		} finally {
			setIsSavingIngredient(false);
		}
	};

	if (isLoading) {
		return (
			<main className="recipe-update-page">
				<div className="recipe-update-container">
					<h1>Loading recipe...</h1>
				</div>
			</main>
		);
	}

	if (!recipe) {
		return (
			<main className="recipe-update-page">
				<div className="recipe-update-container">
					<h1>Recipe not found</h1>
				</div>
			</main>
		);
	}

	return (
		<main className="recipe-update-page">
			{/* Cover Image Upload */}
			<div className="recipe-cover-section">
				<input
					type="file"
					ref={fileInputRef}
					onChange={handleImageChange}
					accept="image/*"
					style={{ display: 'none' }}
				/>

				{!coverImage ? (
					<div
						className="recipe-cover-placeholder"
						onClick={handleImageClick}
					>
						<div className="recipe-cover-placeholder-content">
							<span className="recipe-cover-icon">📷</span>
							<span className="recipe-cover-text">Add Cover Image</span>
							<span className="recipe-cover-subtext">Click to upload</span>
						</div>
					</div>
				) : (
					<div className="recipe-cover-image-container">
						<img
							src={coverImage}
							alt="Recipe cover"
							className="recipe-cover-image"
						/>
						<button
							className="recipe-cover-remove"
							onClick={handleRemoveImage}
							type="button"
						>
							✕
						</button>
						<div className="recipe-cover-buttons">
							<button
								className="recipe-cover-change"
								onClick={handleImageClick}
								type="button"
							>
								Change Image
							</button>
							{selectedFile && (
								<button
									className="recipe-cover-confirm"
									onClick={handleConfirmImage}
									disabled={isUploadingImage}
									type="button"
								>
									{isUploadingImage ? 'Uploading...' : '✓ Confirm'}
								</button>
							)}
						</div>
					</div>
				)}
			</div>

			{/* Recipe Content */}
			<div className="recipe-update-container">
				{/* Title Section */}
				<div className="recipe-title-section">
					{isEditingTitle ? (
						<div className="recipe-title-edit">
							<input
								type="text"
								value={title}
								onChange={(e) => setTitle(e.target.value)}
								className="recipe-title-input"
								placeholder="Recipe title"
							/>
							<div className="recipe-title-buttons">
								<button
									onClick={handleTitleSave}
									disabled={isSavingTitle || !title.trim()}
									className="recipe-title-save"
									type="button"
								>
									{isSavingTitle ? 'Saving...' : '✓ Save'}
								</button>
								<button
									onClick={() => {
										setTitle(recipe.title);
										setIsEditingTitle(false);
									}}
									className="recipe-title-cancel"
									type="button"
								>
									✕ Cancel
								</button>
							</div>
						</div>
					) : (
						<div className="recipe-title-display">
							<h1>{title}</h1>
							<button
								onClick={() => setIsEditingTitle(true)}
								className="recipe-title-edit-btn"
								type="button"
							>
								✎ Edit
							</button>
						</div>
					)}
				</div>

				{/* Ingredients Section */}
				<div className="recipe-ingredients-section">
					<h2>Ingredients</h2>
					<ul className="recipe-ingredients-list">
						{ingredients.map((ingredient, index) => (
							<li key={ingredient.id || index} className="recipe-ingredient-item">
								<span className="ingredient-name">{ingredient.name}</span>
								<span className="ingredient-quantity">
									{ingredient.quantity} {ingredient.unit}
								</span>
							</li>
						))}
						{/* Add Ingredient Button */}
						{!isAddingIngredient ? (
							<li className="recipe-ingredient-add">
								<button
									onClick={() => setIsAddingIngredient(true)}
									className="recipe-ingredient-add-btn"
									type="button"
								>
									+ Add Ingredient
								</button>
							</li>
						) : (
							<li className="recipe-ingredient-form">
								<input
									type="text"
									value={newIngredient.name}
									onChange={(e) => setNewIngredient({ ...newIngredient, name: e.target.value })}
									placeholder="Ingredient name"
									className="ingredient-input ingredient-name-input"
								/>
								<input
									type="text"
									value={newIngredient.quantity}
									onChange={(e) => setNewIngredient({ ...newIngredient, quantity: e.target.value })}
									placeholder="Quantity"
									className="ingredient-input ingredient-quantity-input"
								/>
								<input
									type="text"
									value={newIngredient.unit}
									onChange={(e) => setNewIngredient({ ...newIngredient, unit: e.target.value })}
									placeholder="Unit (e.g., cups, g)"
									className="ingredient-input ingredient-unit-input"
								/>
								<div className="ingredient-form-buttons">
									<button
										onClick={handleAddIngredient}
										disabled={isSavingIngredient}
										className="ingredient-submit-btn"
										type="button"
									>
										{isSavingIngredient ? 'Adding...' : '✓ Add'}
									</button>
									<button
										onClick={() => {
											setIsAddingIngredient(false);
											setNewIngredient({ name: '', quantity: '', unit: '' });
										}}
										className="ingredient-cancel-btn"
										type="button"
									>
										✕ Cancel
									</button>
								</div>
							</li>
						)}
					</ul>
				</div>
			</div>
		</main>
	);
};

export default UpdateRecipePage;
