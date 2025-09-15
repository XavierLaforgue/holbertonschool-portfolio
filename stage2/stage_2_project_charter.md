# PROJECT CHARTER: anime-inspired recipe-sharing website

## Project duration:
Start: August 18, 2025 - End: November 7, 2025

## Author: Xavier Laforgue

## Introduction

The project aims to foster a community of anime fans who are interested in cooking
and experimenting with new recipes inspired by their favorite shows.
The goal is to create a platform
where users can create accounts, share and search for anime-inspired
recipes, leave reviews, and utilize features such as step-by-step instructions,
timers, and recipe personalisations. 
Possible extensions of the project may include meal planning, and
shopping list exports.

## Project objectives (SMART)

The website will provide a professional, engaging, and user-friendly
experience for anime fans who want to share and discover recipes. The
objectives are designed to be SMART: Specific, Measurable, Achievable,
Relevant, and Time-bound.

<!-- ### The objectives
A SMART objective is a well-defined, specific, and measurable objective. It is an acronym that summarizes the five essential characteristics that an objective must have in order to be effective.

* **Specific**:   
The objective must be clear and precise, with a single, clearly defined goal that is targeted and unambiguous. It must formalize what needs to be achieved, who needs to be involved, and by what means.

* **Measurable**:  
It must be quantifiable. A quantified objective indicates concretely whether additional resources or efforts are needed to achieve it. For example, tracking the number of registered users or recipes shared.

* **Achievable**:  
It must be realistic and feasible, considering available skills, time, and resources. Objectives should be motivating but not overly ambitious.

* **Relevant**:  
The objective must be important to the overall project and have proven potential for impact within the anime fan community.

* **Time-bound:**  
The objective must have a clearly defined deadline for completion, allowing for close operational monitoring and steady progress. -->

<!-- ### Objective #1

* Achieve 100 registered users within 6 months of website launch, to build an active community of anime fans interested in cooking.
	* Specific: Grow the user base to 100 registered members.
	* Measurable: Track the number of registered users.
	* Achievable: Promote the site in anime forums and social media groups.
	* Relevant: A strong user base is essential for content generation and community engagement.
	* Time-bound: 6 months after launch.

### Objective #2

* Reach 50 recipes shared by users within 6 months, to ensure a diverse and engaging content offering.
	* Specific: Users share at least 50 recipes.
	* Measurable: Count the number of recipes submitted.
	* Achievable: Encourage contributions through incentives and easy-to-use submission forms.
	* Relevant: Recipe content is central to the platform’s value.
	* Time-bound: 6 months after launch.

### Objective #3

* Implement a meal planner and shopping list export feature within 3 months of launch, to enhance user experience and utility.
	* Specific: Develop and deploy meal planner and shopping list features.
	* Measurable: Features available and functional for all users.
	* Achievable: Use existing libraries and frameworks to accelerate development.
	* Relevant: These features differentiate the site and add practical value.
	* Time-bound: 3 months after launch. -->


### Objective #1

* Deliver a fully functional user registration and authentication system, enabling users to securely create accounts and log in.
	* Specific: User registration and login features are implemented and tested.
	* Measurable: All acceptance criteria for account creation, authentication, and password management are met.
	* Achievable: Developed using secure, well-documented libraries and frameworks.
	* Relevant: Essential for user participation and personalized features.
	* Time-bound: Completed and ready on the first week of development.

### Objective #2

* Provide a recipe submission and search platform, allowing users to add, browse, and search for anime-inspired recipes with step-by-step instructions and optional images/timers.
	* Specific: Recipe submission, browsing, and search functionalities are implemented and tested.
	* Measurable: All acceptance criteria for recipe creation, display, and search are satisfied.
	* Achievable: Developed with user-friendly forms and robust search capabilities.
	* Relevant: Central to the website's purpose and user engagement.
	* Time-bound: Completed and ready on the third week of development.

### Objective #3

* Ensure the website is responsive and accessible, providing a seamless experience across devices and meeting basic accessibility standards.
	* Specific: Responsive design and accessibility features are implemented and verified.
	* Measurable: Passes device compatibility and basic accessibility tests.
	* Achievable: Utilizes modern frameworks and best practices for web design.
	* Relevant: Expands reach and usability for all users.
	* Time-bound: Completed and ready at project delivery.

## Stakeholders and roles

Stakeholders are individuals or groups of individuals whose interests
may be affected by the execution of a project. 
Identifying and managing stakeholders increases the project’s chances of success.

stakeholRecognized stakeholders:

* Anime fans and home cooks (external stakeholders)
* Content creators (external stakeholders)
* Development team (internal stakeholder)
* Tutor (internal stakeholder)

### 1. Anime fans and home cooks

End users who will register, share, and search for recipes. Their feedback and engagement are crucial for the platform's success.

Responsibilities:
Provide feedback, share recipes, use meal planner and shopping list features, and participate in the community.

### 2. Content creators

Users who actively contribute recipes and content, helping to grow the site's offerings.

Responsibilities:
Submit recipes, provide images and instructions, and help moderate content if needed.

### 3. Development team (Project Manager, Functional Lead, Technical Lead)

As the sole member, I am responsible for all aspects of the project, from planning and development to deployment and maintenance.

### 4. Tutor

The local Holberton School Software Engineer ([Sacha
Schoumiloff](https://github.com/SChoumiloff)), responsible for providing
regular feedback, advic, and guidance during all stages of the project execution.

<!-- | Role | Description | Responsibilities |
| ----- | ----- | ----- |
| Anime fans & home cooks | Main users of the site | Register, share/search recipes, use features, provide feedback |
| Content creators | Contributors to site content | Submit recipes, images, instructions, moderate content |
| Development team (Project Manager, Functional Lead, Technical Lead) | Responsible for design, development, and delivery | Plan, define requirements, develop, test, deploy, maintain | -->

## Project scope

Project scope establishes the boundaries of the project by specifying
what will and will not be delivered. It details the features, tasks,
deliverables, and resources required to fulfill the project objectives
and clarifies any exclusions to prevent misunderstandings and waste of ressources.

The aim of the project is to provide anime fans with a unique platform for sharing and discovering recipes inspired by their favorite shows, fostering creativity and community.

### In-scope (what will be delivered)

* User registration and authentication
* Recipe submission and search functionality
* Step-by-step instructions with optional images and timers
* Responsive website design

### Out-scope (what will not be delivered)

* Meal planner and shopping list export features
* Dedicated mobile app (only responsive web design)
* Advanced social networking features (e.g., messaging, forums)

## Risks and mitigation plans

Risk analysis is the process of identifying possible events or conditions that could negatively impact the project, evaluating their likelihood and potential consequences, and developing strategies to minimize or address these risks.

### Technical risks

* Integration issues with third-party libraries or frameworks
	* Solution: Research and test libraries before integration
* Bugs and feature failures
	* Solution: Implement unit and integration tests, use version control
* Security vulnerabilities
	* Solution: Use secure authentication libraries and follow best practices

### Timeline risks

* Underestimating development time
	* Solution: Break tasks into smaller milestones, focus on the
	minimal acceptable deliverable, and reassess progress regularly
* Missing deadlines
	* Solution: Set realistic deadlines and adjust schedule as needed

### Human risks

* Skill gaps or lack of experience with required technologies
	* Solution: Allocate time for learning, seek mentorship, and use
	reliable resources
* Risk of burnout due to workload or time pressure
	* Solution: Set achievable goals, take regular breaks, and monitor
	workload

## Timeline, milestones, and deliverables

This section outlines the project schedule, listing key stages, milestones, and expected deliverables. It provides a clear roadmap to track progress and ensure timely completion of all objectives.

* **Weeks 1 - 2**: Idea development (Completed).
	* Evaluate ideas for feasibility and impact.
		* *Milestone* (week 2): List of ideas and feasibility arguments.
	* Select MVP concept.
		* *Deliverable* (week 2): Stage 1 report with documented idea
		  brainstorming and evaluation, and presentation of selected MVP.

* **Weeks 3 - 4**: Project charter development (In progress).
	* Set SMART objectives.
		* *Milestone* (week 4): Describe 2-3 objectives and their fulfillment of
		  the SMART principles.
	* Risk assessment and mitigation.
	* Establish project scope.
		* *Deliverable* (week 4): Stage 2 report with SMART objectives, risk
		  analyses and definition of the project's scope.

* **Weeks 5 - 6**: Technical documentation
	* Create diagrams and plan system architecture.
		* *Milestone* (week 5-6): Package, class, sequence, and
		  entity-relationship diagrams.
	* Provide rationale for selected technologies.
		* *Deliverable* (week 6): Stage 3 report.

* **Weeks 7 - 10**: MVP development
	* Design and implement data models with persistence in database.
		* *Milestone* (week 7): Class instances persist in the
		  database, tests are available.
	* Develop APIs and add authentication.
		* *Milestone* (week 8-9): Functional endpoints for all basic
		  operations, tests are available. 
	* Construct the user interface components.
		* *Milestone* (week 9): Existent user interface for basic site
		  content and operations.
	* Test all functionalities as a user, improve responsiveness and
	UX.
		* *Devilverable* (week 10): Completed website.

* **Weeks 11 - 12**: Project closure
	* Prepare final presentation.
		* *Milestone* (week 11): A practice presentation providing a sales pitch, a
		  description of the project with timeline and objectives, a
		  discussion of the systems architecture and technical choices,
		  and a demonstration of the
		  website functionalities.
	* Demo day.
		* *Deliverable* (week 12): Final presentation. 
