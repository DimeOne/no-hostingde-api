FROM certbot/certbot:latest

ADD . /app/hostingde-api

RUN pip install -e /app/hostingde-api

VOLUME /run/secrets

ENTRYPOINT ["/usr/local/bin/certbot", "-a", "dns-hostingde", "--dns-hostingde-credentials", "/run/secrets/credentials.ini", "--dns-hostingde-propagation-seconds", "60"]
