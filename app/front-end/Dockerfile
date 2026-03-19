# =============================================================================
# Front-end Dockerfile: React SPA built with Vite
# =============================================================================
#
# This is a multi-stage build:
#   Stage 1 ("build"): Install dependencies and build the production bundle.
#   Stage 2 ("runtime"): A minimal image that only holds the built files.
#
# Why not serve with Nginx directly in this image?
#   We have a dedicated Nginx service that also handles API proxying and
#   load balancing, so this image only needs to produce the build output.
#
# Build context: ./front-end
# =============================================================================

# ========================
# Stage 1: Build
# ========================

# Small image with Node.js LTS for fast builds.
FROM node:20-alpine AS build

WORKDIR /app

# Copy dependency manifests first for Docker layer caching.
# This layer is only rebuilt when package.json or package-lock.json change.
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the source code and build the production bundle.
# VITE_API_BASE_URL is set to "" (empty string) because in production
# the front-end and API live behind the same Nginx reverse proxy, so
# all API calls use relative URLs (same origin).
COPY . .
ARG VITE_API_BASE_URL=""
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
RUN npm run build

# The final image does NOT contain node_modules or source code, only
# the optimized static files in `dist/`. This dramatically reduces
# image size.

# ========================
# Stage 2: Runtime
# ========================
# Minimal image just to hold the built files.
# The container does not need to run a server. Nginx reads the files
# from a shared Docker volume.
FROM alpine:3.21

WORKDIR /app/dist

# Copy only the build output from stage 1.
COPY --from=build /app/dist .
# /app/dist will be mounted as volume while composing so the
# Nginx container can serve these files.

# This container's sole purpose is to populate the shared volume with
# the built front-end files. 
# `tail -f /dev/null` is a common lightweight "do nothing" pattern.
CMD ["tail", "-f", "/dev/null"]
# This instruction starts the container and keeps it alive so Docker
# Compose keeps the volume mounted, while consuming virtually zero
# resources.
