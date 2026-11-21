npm run build;

npm vite build --watch &
WATCH_PID=$!
trap "kill $WATCH_PID; docker compose down;" EXIT

docker compose up --build --watch;
