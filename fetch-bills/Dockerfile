FROM ubuntu:latest

LABEL name="siw36/the-lazy-consultant:fetch-bills" \
  maintainer="https://github.com/siw36" \
  version="1" \
  release="1" \
  summary="Automatically gather bills for travel expense calculation" \
  description="Automatically gather bills for travel expense calculation" \
  url="https://github.com/siw36/the-lazy-consultant"

ARG FIREFOX_VERSION=73.0.1
ARG FIREFOX_LINK=https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2
ARG GECKODRIVER_VERSION=v0.26.0
ARG GECKODRIVER_LINK=https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

ENV HOME=/home/selenium \
  LC_ALL=en_US.UTF-8 \
  LANG=en_US.UTF-8 \
  LANGUAGE=en_US.UTF-8 \
  TZ=Europe/Berlin \
  PYTHONUNBUFFERED=1

USER 0

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
  curl \
  tar \
  gzip \
  ca-certificates \
  python3 \
  python3-pip \
  fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
  libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
  xvfb

# Dependencies
RUN pip3 install setuptools \
  && pip3 install \
  configparser \
  selenium \
  webdavclient3 \
  pyvirtualdisplay

# Firefox
RUN curl -sL $FIREFOX_LINK | tar -C /var/lib/ -xvj && \
  ln -s /var/lib/firefox/firefox /usr/bin/firefox

# Geckodriver
RUN curl -sL $GECKODRIVER_LINK | tar -C /usr/bin/ -xvz

# Configuration
RUN update-ca-certificates \
  && mkdir -p $HOME

# Cleanup
RUN apt-get purge -y curl \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# Copy app
COPY *.py $HOME/

# Permissions
RUN chgrp -R 0 $HOME \
  && chmod -R g=u $HOME \
  && chmod -R 775 $HOME

USER 1001

WORKDIR $HOME

ENTRYPOINT [ "python3", "main.py" ]
