#!/bin/bash

docker run -it --name fetch-bills \
  --mount type=bind,source="$(pwd)"/config.ini,target=/home/selenium/config.ini \
  fetch-bills:latest
