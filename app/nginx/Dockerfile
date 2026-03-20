# =============================================================================
# Nginx Dockerfile — reverse proxy and static file server
# =============================================================================
#
# At runtime, Docker Compose mounts three volumes into this container:
#   /var/www/frontend/  — built React SPA files (from front-end service)
#   /var/www/static/    — Django collected static files (from back-end)
#   /var/www/media/     — user-uploaded media files (from back-end)
#
# Build context: ./nginx
# =============================================================================

# Small, production-ready Nginx image based on Alpine Linux (~10 MB).
FROM nginx:stable-alpine

# Remove the default Nginx site configuration and replace it with ours
# (proxy + SPA serving + load balancing setup).
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
