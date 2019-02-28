FROM certbot/certbot

ADD . /app/hostingde-api

RUN pip install -e /app/hostingde-api

VOLUME [/run/secrets/hosting.de]

ENTRYPOINT ["certbot" "-a" "no-hostingde-api:dns-hostingde" "--no-hostingde-api:dns-hostingde-credentials" "/run/secrets/hosting.de/credentials.ini" "--no-hostingde-api:dns-hostingde-propagation-seconds" "60"]
