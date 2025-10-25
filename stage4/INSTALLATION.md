# Animize-eat setup guide
This application has been dockerized.

## Prerequisites
To install/run **animize-eat** you need the docker engine and CLI, i.e., the following terminal commands should return the installed versions.
```bash
docker --version; docker-compose --version
```
If anything other than the program versions is output then install docker (e.g., https://docs.docker.com/get-started/) before resuming this guide.

The application has been tested with:
```
Docker version 28.3.3, build 980b856
Docker Compose version v2.39.2-desktop.1
```

## Start guide
### 1. Clone repository
Clone the repository to the desired directory:
```bash
git clone https://github.com/XavierLaforgue/holbertonschool-portfolio.git ./desired-directory
cd desired-directory/stage4/
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
