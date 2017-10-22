
FROM homeassistant/home-assistant:0.56.1
MAINTAINER Julian Kahnert <mail@juliankahnert.de>
LABEL org.freenas.version="0.56.1" \
      org.freenas.upgradeable="true" \
      org.freenas.autostart="true" \
      org.freenas.web-ui-protocol="http" \
      org.freenas.web-ui-port=8123 \
      org.freenas.web-ui-path="states" \
      org.freenas.expose-ports-at-host="true" \
      org.freenas.port-mappings="8123:8123/tcp" \
      org.freenas.volumes="[ \
          { \
              \"name\": \"/config\", \
              \"descr\": \"Home-Assistant config\" \
          } \
      ]"\
      org.freenas.settings="[ \
          { \
              \"env\": \"TZ\", \
              \"descr\": \"homeassistant Container Timezone\", \
              \"optional\": true \
          } \
      ]"

RUN pip install bs4 lxml

RUN echo "deb http://apt.pilight.org/ stable main" > /etc/apt/sources.list.d/pilight.list && \
    wget -O - http://apt.pilight.org/pilight.key | apt-key add - && \
    apt-get update && \
    apt-get install -y --force-yes --no-install-recommends pilight && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8123
    