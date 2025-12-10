# Use an NGINX base image
FROM nginx:alpine

# Remove the default NGINX HTML files
RUN rm -rf /usr/share/nginx/html/*

# Copy the custom HTML, CSS, JavaScript, and icon files
COPY index.html /usr/share/nginx/html/index.html
COPY static /usr/share/nginx/html/static

# Expose the default NGINX port
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]

