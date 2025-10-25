# Animize-eat setup guide
This application has been dockerized.
The setup instructions provided below have been written for and tested on Ubuntu-22.04, but they are expected to work on any Unix-based system.

## Prerequisites
To install/run **animize-eat** you need the docker engine and CLI, i.e., the following terminal commands should return the installed version.
```bash
docker --version
```
If anything other than the program version is output then install docker (e.g., https://docs.docker.com/get-started/) before resuming this guide.

The application has been tested with: `Docker version 28.3.3, build 980b856`

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

### 4. Import media files
No image broker has been implemented yet, Django is still in charge of delivering them.
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
	|_.env.dev,Dockerfile.dev,manage.py,.dockerignore,requirements.txt,download_media.sh
```
Alternatively, use the provided bash script: `download_media.sh` making sure it has execution permissions (still from `stage4/`):
```bash
chmod +x backend/download_media.sh
./backend/download_media.sh
```
### 5. Build and start services

#### 5.1 Single-service testing: build and start only backend
Change directory to `backend`, build and start the container
```bash
cd backend
docker build -f Dockerfile.dev -t backend:dev .
```

