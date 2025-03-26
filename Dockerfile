FROM python:3.8.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tuoteselosteet

RUN apt-get update && apt-get install -y --no-install-recommends \
    apache2 \
    apache2-dev \
    openssl \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir mod_wsgi \
    && mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load \
    && a2enmod wsgi ssl

COPY tuoteselosteet/server.crt /etc/ssl/certs/server.crt
COPY tuoteselosteet/server.key /etc/ssl/private/server.key
    
COPY tuoteselosteet/requirements.txt /tuoteselosteet/requirements.txt

RUN pip install --no-cache-dir -r /tuoteselosteet/requirements.txt

COPY tuoteselosteet/ /tuoteselosteet
COPY apache/000-default.conf /etc/apache2/sites-available/000-default.conf

EXPOSE 443

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apachectl", "-D", "FOREGROUND"]