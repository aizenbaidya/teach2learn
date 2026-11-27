docker build -t teach2learn-image .
docker run --rm -p 1234:5000 --name teach2learn-container teach2learn-image
