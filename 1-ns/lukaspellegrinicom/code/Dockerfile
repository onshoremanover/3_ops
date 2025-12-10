FROM php:8.2-apache

# PHP extensions you likely need
RUN docker-php-ext-install mysqli pdo pdo_mysql \
  && a2enmod rewrite headers expires

# Optional: suppress FQDN warning
RUN printf "ServerName localhost\n" > /etc/apache2/conf-available/servername.conf \
  && a2enconf servername

# Copy your site (we already confirmed docroot content lives in ./site)
COPY src/ /var/www/html/

# Make sure Apache can read the files
RUN chown -R www-data:www-data /var/www/html
