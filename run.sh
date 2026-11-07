docker build -t teach2learn .
# docker run --rm --env-file .env -p 5000:5000 teach2learn
docker run --rm -p 5000:5000 teach2learn
