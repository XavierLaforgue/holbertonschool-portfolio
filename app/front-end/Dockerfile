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

# Copy only the build output from stage 1, into /build.
# /build is deliberately NOT the folder where the shared volume is mounted
# (/app/dist, see compose.prod.yml): a volume hides whatever the image has
# at its mount point, so files stored there would only reach a brand-new
# volume and a rebuilt image would never replace them.
COPY --from=build /app/dist /build

# Create the mount point of the shared volume (also the working directory).
WORKDIR /app/dist

# On every start (`sh -c "..."` runs the three commands in order):
#   1. `rm -rf /app/dist/*` empties the shared volume (the files of the
#      previous build, whose names change on every build),
#   2. `cp -a /build/. /app/dist/` copies this image's files into it
#      (`-a` keeps the files' attributes, `/.` copies the folder's content),
#   3. `exec tail -f /dev/null` then does nothing forever: a common
#      lightweight pattern that keeps the container alive, so Docker
#      Compose keeps the volume mounted, at virtually zero cost (`exec`
#      makes it replace the shell, so `docker compose stop` stops it
#      at once).
# So `docker compose up --build` is enough to serve a new front-end build.
CMD ["sh", "-c", "rm -rf /app/dist/* && cp -a /build/. /app/dist/ && exec tail -f /dev/null"]
