# Animize-eat setup guide
This application has been dockerized.
The setup instructions provided below have been written for and tested on Ubuntu-22.04, but they are expected to work on any Unix-based system.

## Prerequisites
To install/run **animize-eat** you need the docker engine and CLI, i.e., the following terminal commands should return the installed version.
```bash
docker --version
docker compose version
```
If anything other than the program version is output then install docker (e.g., https://docs.docker.com/get-started/) before resuming this guide.

The application has been tested with: 
```bash
Docker version 28.3.3, build 980b856
Docker Compose version v2.39.2-desktop.1
```
and it is known to require Docker Compose V2+.

## Start guide
### 1. Clone repository
Clone the repository to the desired directory:
```bash
git clone --branch main https://github.com/XavierLaforgue/holbertonschool-portfolio.git ./desired-directory
cd desired-directory/stage4
```

### 2. Provide environment file (backend)
Use the provided `backend/.env.dev.example` to create a private `backend/.env.dev` file the backend (Django) will actually use.
#### 2.1. Secret key
Provide a secret key for Django to use for all cryptographic needs (secure sessions, cookies, tokens, etc).
A random key could be generated, e.g., 
- using Python: 
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
- or openSSL:
```bash
openssl rand -base64 50
```
#### 2.2. Database configuration
Provide the desired database configuration.
### 3. Provide environment file (frontend)
Use the provided `frontend/animize_eat/.env.dev.example` to create a private `frontend/animize_eat/.env.dev` file the frontend (React) will actually use.
### 4. Provide environment file (composed app)
Now that `.env.dev` files are available for backend and frontend, execute the bash script
```bash
./combine-env-files.dev.sh
```
to combine them into a single file (`.env.combined.dev`) with all environment variables (or just copy-paste into one).
### 4. Import media files
No image broker (object storage, e.g., `S3`) has been implemented yet, Django is still in charge of delivering them.
As to not upload the media files to github, they are provided in the google drive: https://drive.google.com/drive/folders/1tCYiEiYwLagJAN0OKQOdKivf30HSud_F?usp=sharing.
Download the media directory into the backend directory so the resulting structure is:
```
|_backend/
	|-accounts/
		|_...
	|-animmize_eat/
		|_...
	|-media/
		|_avatars/
			|_...
	|-tokens/
		|_...
	|_.env.dev,Dockerfile.dev,manage.py,.dockerignore,requirements.txt,download_media.sh,...
```
Alternatively, use the provided bash script: `download_media.sh` making sure it has execution permissions (still from `stage4/`):
```bash
cd backend
chmod +x download_media.sh
./download_media.sh
cd ..
```
**Warning**: the script is slow and will not work if the folder contains more than 50 files.
### 5. Build and start services
To build image and launch container with the composed app run:
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml up --build
```
**Note:** the variables provided by `--env-file .env.combined.dev` are only available to docker-compose itself (for variable substitution in the compose file), but they are now also passed into the backend container via the `environment` section in compose.dev.yaml.

#### 5.0 Build and start with hot reload
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml watch --build
```
#### 5.1 Stop the container
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml down
```
#### 5.2 Launch the container in the background
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml up --build -d
```
#### 5.3 Examine logs in real-time 
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml logs -f
```
#### 5.4 Examine the logs of a single service
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml logs -f <service>
```
#### 5.5 Access the shell of a service running in the container
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml exec <service-name> sh
```
- For the backend:
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml exec backend sh
```
- For the frontend:
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml exec frontend sh
```
- For the reverse proxy:
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml exec reverse-proxy sh
```
- For the database:
```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml exec db sh
psql -d <DB_NAME> -U <DB_USERNAME> -h <DB_HOST> -p <DB_PORT>
```


<!-- #### 5.1 Single-service testing: build and start only backend
Change directory to `backend`, build and start the container
```bash
cd backend
docker compose --env-file .env.dev -f compose.dev.yaml up --build
```
It is setup to create the images, launch the containers, create the database and populate it, and launch the development server on `localhost:8000`.

In case we need to access the shell inside the backend container we use (in another terminal, in the same directory, while the first is active with the stdout of the running container):
```bash
docker compose --env-file .env.dev -f compose.dev.yaml exec backend bash
```
#### 5.2 Single-service testing: build and start only frontend
Change directory to `frontend/animize_eat`, build and start the container
```bash
cd frontend/animize_eat
docker compose --env-file .env.dev -f compose.dev.yaml up --build
```
In case we need to access the shell inside the frontend container we use (in another terminal, in the same directory, while the first is active with the stdout of the running container):
```bash
docker compose --env-file .env.dev -f compose.dev.yaml exec frontend sh
```
#### 5.3 Single-service testing: build and start only reverse-proxy
Change directory to `reverse-proxy`, build and start the container
```bash
cd reverse-proxy
docker compose -f compose.dev.yaml up --build
```
In case we need to access the shell inside the frontend container we use (in another terminal, in the same directory, while the first is active with the stdout of the running container):
```bash
docker compose -f compose.dev.yaml exec reverse-proxy sh
``` -->
