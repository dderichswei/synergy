#!/bin/bash

docker build -t "ddsynergy:1" .
docker run -d --name "ddsynergy" --restart unless-stopped -v ~/synergy/:/home/notebook/notebooks -p 8888:8888 ddsynergy:1
docker logs -f ddsynergy
