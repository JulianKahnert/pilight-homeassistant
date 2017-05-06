#!/usr/bin/env python3
import os
import bs4
import requests
import re
import subprocess

url = 'https://hub.docker.com/r/homeassistant/home-assistant/tags/'

# get ha tags from docker hub
sess = requests.session()
r = sess.get(url, allow_redirects=True)
soup = bs4.BeautifulSoup(r.text, 'html.parser')
table = soup.find_all('div', attrs={'class': 'FlexTable__flexRow___2mqir'})

tags_docker = []
for row in table:
    tag = row.find_all('div', attrs={'class': 'FlexTable__flexItem___3vmPs'})[0].string
    tags_docker += [tag]
tags_docker = set(tags_docker)

# get local tags
raw = subprocess.run(['git', 'tag'], stdout=subprocess.PIPE)
tags_local = raw.stdout.decode('utf-8').split('\n')[:-1]
tags_local += ['latest']
tags_local += ['dev']
tags_local = set(tags_local)

# create a new commit
tags_to_update = list(tags_docker - tags_local)
tags_to_update.sort()
for tag in tags_to_update:
    # generate new docker file
    print('\n\nprocessing tag: {}'.format(tag))
    dockerfile = """
FROM homeassistant/home-assistant:{}
MAINTAINER Julian Kahnert <mail@juliankahnert.de>
LABEL org.freenas.version="{}" \\
      org.freenas.upgradeable="true" \\
      org.freenas.autostart="true" \\
      org.freenas.web-ui-protocol="http" \\
      org.freenas.web-ui-port=8123 \\
      org.freenas.web-ui-path="states" \\
      org.freenas.expose-ports-at-host="true" \\
      org.freenas.port-mappings="8123:8123/tcp" \\
      org.freenas.volumes="[ \\
          {{ \\
              \\"name\\": \\"/config\\", \\
              \\"descr\\": \\"Home-Assistant config\\" \\
          }} \\
      ]"\\
      org.freenas.settings="[ \\
          {{ \\
              \\"env\\": \\"TZ\\", \\
              \\"descr\\": \\"homeassistant Container Timezone\\", \\
              \\"optional\\": true \\
          }} \\
      ]"

RUN pip install bs4 lxml

RUN echo "deb http://apt.pilight.org/ stable main" > /etc/apt/sources.list.d/pilight.list && \\
    wget -O - http://apt.pilight.org/pilight.key | apt-key add - && \\
    apt-get update && \\
    apt-get install -y --force-yes --no-install-recommends pilight && \\
    rm -rf /var/lib/apt/lists/*

EXPOSE 8123
    """.format(tag, tag)
    f = open('Dockerfile', 'w')
    f.write(dockerfile)
    f.close()

    # v="0.42" && git commit --all --message "Version $v" && git tag $v && git push --tags
    subprocess.run(['git', 'commit', '--all', '--message', 'Version {}'.format(tag)])
    subprocess.run(['git', 'tag', tag])
    subprocess.run(['git', 'push', '--tags', 'public', 'master'])
