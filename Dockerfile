
FROM homeassistant/home-assistant:0.38
MAINTAINER Julian Kahnert <mail@juliankahnert.de>
LABEL org.freenas.version="0.38" \
      org.freenas.upgradeable="true" \
      org.freenas.autostart="true" \
      org.freenas.expose-ports-at-host="true" \
      org.freenas.port-mappings="8123:8123/udp,8123:8123/tcp" \
      org.freenas.volumes="[ \
          { \
              \"name\": \"/config\", \
              \"descr\": \"Home-Assistant config\" \
          } \
      ]"

RUN pip install bs4 lxml

RUN echo "deb http://apt.pilight.org/ stable main" > /etc/apt/sources.list.d/pilight.list && \
    wget -O - http://apt.pilight.org/pilight.key | apt-key add - && \
    apt-get update && \
    apt-get install -y --no-install-recommends pilight && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8123
    