#!/bin/bash

docker build -t teach2learn .
docker run --rm -p 8000:8000 -e PORT=8000 teach2learn
