# Dockerfile
FROM nginx:alpine

# Remove default nginx static content
RUN rm -rf /usr/share/nginx/html/*

# Copy our static files
COPY index.html style.css app.js /usr/share/nginx/html/

# Nginx listens on 80 by default
EXPOSE 80

# No CMD needed — default nginx startup used