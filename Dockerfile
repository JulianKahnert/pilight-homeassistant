FROM homeassistant/home-assistant:0.40.1
MAINTAINER Julian Kahnert <mail@juliankahnert.de>

RUN pip install bs4 lxml

RUN echo "deb http://apt.pilight.org/ stable main" > /etc/apt/sources.list.d/pilight.list && \
    wget -O - http://apt.pilight.org/pilight.key | apt-key add - && \
    apt-get update && \
    apt-get install -y --no-install-recommends pilight && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8123
