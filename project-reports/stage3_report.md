# Portfolio project - Stage 3: Technical Documentation
This documentation is meant to provide a detailed technical plan for the
development of the MVP, namely, an anime-inspired recipe-sharing
website.

## User stories and mockups

### User stories
The following are a list of **User Stories** in line with the
MVP, categorized by priority using the MoSCoW method:

#### Must have
- *As **an anime fan and a home cook**, I want to <u>create and log-in to an account</u> so that <u>I can save my favorite anime-inspired recipes</u>.*
- *As **a home cook**, I want to <u>browse and search for recipes</u> so that I can <u>find new meals to try</u>.*
- *As **a content creator**, I want to <u>submit and share anime-inspired recipes of my own creation with step-by-step instructions and images</u> so that <u>others can follow and recreate it</u>.*
- *As **any user**, I want to <u>experience a responsive and dynamic platform</u> so that <u>I can be comfortable and use the website with ease on any device</u>.*
  
#### Should have
- *As **an anime fan and a home cook**, I want to <u>filter recipes by ingredient, number of ingredients, preparation time, difficulty, and anime of inspiration</u> so that <u>I can find recipes that suit my needs</u>.*
- *As **a home cook**, I want to <u>leave reviews and ratings on recipes</u> so that <u>I can share feedback and help others choose</u>.*
- *As **a home cook**, I want to <u>adjust quantity of ingredients according to the desired number of portions</u> so that <u>I can cook for any number of people</u>.*
- *As **a home cook**, I want to <u>have a countdown timer already programmed with each step duration</u> such that <u>I won't need any other support tools (besides the cooking utensils, of course) other than the website to track the progress and simplify following the recipe</u>.*

#### Could have
- *As **a home cook**, I want to <u>bookmark or favorite recipes</u> so that <u>I can easily find them later</u>.*
- *As **a home cook**, I want to <u>follow other users or content creators</u> so that <u>I can see their latest recipes</u>.*

#### Won't have (for MVP)
- *As **a home cook**, I want to <u>view detailed nutritional information for each recipe</u> so that <u>I can make informed choices</u>.*
- *As **a home cook**, I want to <u>create a meal plan from selected recipes</u> so that <u>I can organize my weekly cooking</u>.*
- *As **a home cook**, I want to <u>export a shopping list based on my meal plan</u> so that <u>I can shop efficiently</u>.*
- *As **any user**, I want to <u>send direct messages to other users</u> so that <u>I can discuss recipes privately</u>.*
- *As **any user**, I want to <u>participate in forums or group chats</u> so that <u>I can engage in community discussions</u>.*
- *As **any user**, I want to <u>have access to a dedicated mobile app</u> so that <u>I can use the platform offline</u>.*

### Mockups

## System architecture
![High-level architecture diagram](./stage3_tasks/Diagrams-Architecture.drawio.png)

The system follows the typical architecture of a web application with a graphical UI.
Users may use desktop or mobile devices to access the web site communicating securely with a reverse proxy.
The reverse proxy redirects the requests to the front-end or the back-end, accordingly.
The front-end and back-end servers may be instantiated multiple times, scaling the service to satisfy demand.
The back-end uses external services to store user files, such as images, and to fill the database of recipe ingredients and anime titles.

## Components, classes, and database design
### Class diagram
%% #TODO: update class diagram to match new ER diagram 
```mermaid
classDiagram
    class BaseEntity {
        +id: UUID
        +created_at: DateTime
        +updated_at: DateTime
        +deleted_at: DateTime
        +is_active: Bool
        +is_staff: Bool
        +soft_delete()
    }

    %% User accounts
    BaseEntity <|-- User : extends

    class User {
        +username: String
        +email: String
        +password_hash: String
        +is_admin: Bool
        +login()
        +logout()
    }

    %% User profiles
    BaseEntity <|-- Profile : extends

    class Profile { 
        +display_name: String
        +bio: String
        +avatar_url: String
        +favorite_anime: String
        %% +posted_recipes: List[Recipe]
        %% +drafted_recipes: List[Recipe]
        %% +saved_recipes: List[Recipe]
    }

    User "1" *--> "1" Profile : has

    %% Recipes
    BaseEntity <|-- Recipe : extends

    class Recipe {
        +title: String
        +description: String
        +difficulty: Difficulty
        +portions: Integer
        +total_time: Duration
        +status: RecipeStatus 
        +published_at: DateTime
        +publish()
        +retract()
        +save()
    }

    Profile "1" *--> "0..*" Recipe : manages

    BaseEntity <|-- RecipePhoto : extends

    Recipe "1" *--> "0..4" RecipePhoto : includes
 
    class RecipePhoto {
        +order: Integer
        +photo_url: String
        *comment: String
    }

    %% Ingredients
    BaseEntity <|-- Ingredient : extends

    class Ingredient {
        +name: String
        +unit: String
    }

    BaseEntity <|-- RecipeIngredient : extends

    class RecipeIngredient {
        +ingredient: Ingredient
        +quantity: Float
    }

    Recipe "1" --> "1..*" RecipeIngredient : uses
    RecipeIngredient "*" --> "1" Ingredient : references

    %% Steps
    BaseEntity <|-- Step : extends

    class Step {
        +order: Integer
        +description: String
        +duration: Duration 
    }

    Recipe "1" *--> "0..*" Step : lists

    BaseEntity <|-- Anime : extends
    
    %% Anime
    class Anime {
        +title: String
        +source: String
    }

    Recipe "0..*" <-- "1" Anime : inspires

    %% ===== Enums =====
    class Difficulty {
        <<enumeration>>
        EASY
        MEDIUM
        HARD
    }

    class RecipeStatus {
        <<enumeration>>
        DRAFT
        PUBLISHED
    }
```
### Entity-relationship diagram
```mermaid
erDiagram   
    User[User]:::fontClassName {
        uuid id PK
        str username UK
        str email UK
        str first_name
        str last_name
        date birth_date
        str password_hash
        bool is_superuser
        bool is_active
        bool is_staff
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    User ||--|| Profile : has

    Profile[Profile]:::fontClassName {
        uuid id PK
        uuid user_id FK "User.id"
        str display_name UK
        str bio
        str avatar_url
        uuid favorite_anime_id FK "Anime.id"
        str favorite_anime_custom
        str myAnimeList_profile
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    Profile ||--o{ Recipe : manages
    
    Recipe[Recipe]:::fontClassName {
        uuid id PK
        uuid profile_id FK "Profile.id"
        uuid anime_id FK "Anime.id"
        str title
        str description
        str difficulty FK "Difficulty.id"
        int portions
        int preparation_time_minutes
        str status FK "Recipe_Status.id"
        timestamptz published_at
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    Anime ||--o{ Recipe : inspires

    Anime[Anime] {
        uuid id PK
        str title
        str reference_page
    }

    Anime_Db_Version ||--|{ Anime : versions

    Anime_Db_Version[Anime_Db_Version] {
        uuid id PK
        str provider_name
        str provider_version
        timestamptz imported_at
        timestamptz updated_at
    }

    Difficulty ||--o{ Recipe : classifies

    Difficulty {
        uuid id PK
        str value
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    Recipe_Status ||--o{ Recipe : classifies

    Recipe_Status {
        uuid id PK
        str value
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    Recipe_Photo |{--}| Recipe : enriches

    Recipe_Photo {
        uuid id PK
        uuid recipe_id FK "Recipe.id"
        int order UK "(recipe_id, order)"
        str photo_url
        str comment
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    Recipe ||--|{ Recipe_Ingredient : uses

    Recipe_Ingredient {
        uuid id PK
        uuid recipe_id FK "Recipe.id"
        uuid ingredient_id FK "Ingredient.id"
        float quantity
        uuid unit_id FK "Unit.id"
    }

    Recipe_Ingredient }o--|| Ingredient : quantifies

    Ingredient {
        uuid id PK
        str name
        bool is_countable
    }

    Recipe_Ingredient }o--o| Unit : "is measured in"

    Unit {
        uuid id PK
        str name
        str abbreviation
        bool is_countable
    }

    Recipe ||--|{ Step : lists

    Step {
        uuid id PK
        uuid recipe_id FK "Recipe.id"
        int order UK "(recipe_id, order)"
        str description
        int duration_hours
        int duration_minutes
        int duration_seconds
    }
```
