# Diagrams

All technical diagrams for the `animize_eat` project.

## Production Architecture

```mermaid
flowchart TD
    Browser["Browser"]

    Browser -->|"all traffic"| Nginx

    subgraph docker["Docker Compose"]
        Nginx["Nginx :80"]

        Nginx -->|"/api/ & /admin/"| backend1 & backend2 & backendN

        subgraph backend_pool["back-end (gunicorn)"]
            backend1["replica 1"]
            backend2["replica 2"]
            backendN["replica N"]
        end
        
        backend1 & backend2 & backendN --> DB

        DB[("PostgreSQL 18")]
        
        DB --- pg_vol

        pg_vol[/"postgres_data"/]

        Nginx -->|"/ (SPA)"| frontend_vol

        frontend_vol[/"frontend_build"/]

        Nginx -->|"/static/"| static_vol

        static_vol[/"backend_static"/]

        Nginx -->|"/media/"| media_vol

        media_vol[/"backend_media"/]
    end
```

## User Flow

```mermaid
flowchart TD
    Visit["Visit site"] --> Feed["Browse public feed\n(search, filter, sort)"]
    Feed --> ViewRecipe["View recipe detail"]
    Feed --> Auth{"Logged in?"}

    Auth -->|No| LoginSignup["Sign up / Log in"]
    LoginSignup --> AuthDone["Authenticated"]
    Auth -->|Yes| AuthDone

    AuthDone --> MyRecipes["My Recipes dashboard\n(Draft / Ready / Published / Saved)"]
    AuthDone --> SaveCopy["Save/copy a published recipe\n(immutable snapshot)"]

    MyRecipes --> Create["Create new recipe\n(starts as Draft)"]
    MyRecipes --> Edit["Edit existing recipe"]

    Create --> AddContent["Add steps, ingredients, photos"]
    Edit --> AddContent

    AddContent --> Ready["Set status: Ready\n(needs title + anime + 1 ingredient)"]
    Ready --> Publish["Set status: Published\n(needs main photo)"]
    Publish --> Feed
```

## Entity-Relationship Diagram

```mermaid
erDiagram
    CustomUser ||--|| Profile : "has one"

    Profile ||--o{ Recipe : "authors"
    Profile ||--o{ SavedRecipe : "saves"

    Recipe }o--|| RecipeStatus : "has status"
    Recipe }o--o| Difficulty : "has difficulty"
    Recipe ||--o{ Step : "has steps"
    Recipe ||--o{ RecipePhoto : "has photos"
    Recipe ||--o{ RecipeIngredient : "has ingredients"
    Recipe ||--o{ SavedRecipe : "original for"

    SavedRecipe }o--|| RecipeStatus : "has status"
    SavedRecipe }o--o| Difficulty : "has difficulty"
    SavedRecipe ||--o{ SavedStep : "has steps"
    SavedRecipe ||--o{ SavedRecipeIngredient : "has ingredients"
    SavedRecipe }o--o| Profile : "original author"

    RecipeIngredient }o--|| Ingredient : "references"
    RecipeIngredient }o--|| Unit : "measured in"
    SavedRecipeIngredient }o--|| Ingredient : "references"
    SavedRecipeIngredient }o--|| Unit : "measured in"

    Ingredient }o--o{ UnitKind : "allows unit kinds"
    Unit }o--|| UnitKind : "belongs to kind"

    CustomUser {
        UUID id PK
        string email UK "USERNAME_FIELD"
        string username UK
        string first_name
        string last_name
        datetime created_at
        datetime updated_at
        datetime deactivated_at
        datetime deleted_at
    }

    Profile {
        UUID id PK
        UUID user_id FK "OneToOne CustomUser"
        string display_name UK
        date birth_date
        text bio
        string favorite_anime_custom
        string favorite_meal
        string location
        url myAnimeList_profile
        text dietary_preferences
        datetime created_at
        datetime updated_at
        datetime cleared_at
    }

    Recipe {
        UUID id PK
        UUID author_id FK "Profile"
        string title
        string anime_custom
        text description
        UUID difficulty_id FK "Difficulty"
        int portions
        int estimated_time_minutes
        UUID status_id FK "RecipeStatus"
        datetime published_at
        datetime created_at
        datetime updated_at
    }

    SavedRecipe {
        UUID id PK
        UUID saver_id FK "Profile"
        UUID original_recipe_id FK "Recipe nullable"
        UUID original_author_id FK "Profile nullable"
        string title
        string anime_custom
        text description
        UUID difficulty_id FK
        int portions
        int estimated_time_minutes
        UUID status_id FK
        datetime published_at
        datetime saved_at
        datetime created_at
        datetime updated_at
    }

    Step {
        UUID id PK
        UUID recipe_id FK "Recipe"
        int number "unique per recipe"
        text description
        duration duration
        datetime created_at
        datetime updated_at
    }

    SavedStep {
        UUID id PK
        UUID recipe_id FK "SavedRecipe"
        int number "unique per recipe"
        text description
        duration duration
        datetime created_at
        datetime updated_at
    }

    RecipePhoto {
        UUID id PK
        UUID recipe_id FK "Recipe"
        image image "validated size and type"
        int position "1=main 2-5=gallery"
        datetime created_at
        datetime updated_at
    }

    Difficulty {
        UUID id PK
        string label UK
        int value UK
        datetime created_at
        datetime updated_at
    }

    RecipeStatus {
        UUID id PK
        string value UK "Draft|Ready|Published"
        datetime created_at
        datetime updated_at
    }

    Ingredient {
        UUID id PK
        string name UK
    }

    Unit {
        UUID id PK
        string name
        string symbol
        UUID kind_id FK "UnitKind"
    }

    UnitKind {
        UUID id PK
        string label UK "weight|volume|count"
        string descriptive_name
    }

    RecipeIngredient {
        UUID id PK
        UUID recipe_id FK "Recipe"
        UUID ingredient_id FK "Ingredient"
        float quantity
        UUID unit_id FK "Unit"
        datetime created_at
        datetime updated_at
    }

    SavedRecipeIngredient {
        UUID id PK
        UUID recipe_id FK "SavedRecipe"
        UUID ingredient_id FK "Ingredient"
        float quantity
        UUID unit_id FK "Unit"
        datetime created_at
        datetime updated_at
    }
```
