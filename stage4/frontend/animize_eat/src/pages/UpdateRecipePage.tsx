import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/UpdateRecipePage.css';
import { API_BASE_URL } from '../config';

interface Recipe {
	id: string;
	title: string;
	cover_image?: string;
	// Add other recipe fields as needed
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
					// Set cover image if it exists
					if (data.cover_image) {
						setCoverImage(data.cover_image);
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
				<h1>{recipe.title}</h1>
				<p>More interactive elements coming soon...</p>
			</div>
		</main>
	);
};

export default UpdateRecipePage;
