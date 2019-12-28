FROM certbot/certbot:latest

ADD . /app/hostingde-api

RUN pip install -e /app/hostingde-api

VOLUME /run/secrets/hosting.de

ENTRYPOINT ["/usr/local/bin/certbot", "-a", "no-hostingde-api:dns-hostingde", "--no-hostingde-api:dns-hostingde-credentials", "/run/secrets/hosting.de/credentials.ini", "--no-hostingde-api:dns-hostingde-propagation-seconds", "60"]
