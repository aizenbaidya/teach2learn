npm run build;

npx vite build --watch &
WATCH_PID=$!
trap "kill $WATCH_PID; docker compose down;" EXIT

docker compose up --build --watch;
