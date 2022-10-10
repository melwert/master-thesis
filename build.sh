#cd ./frontend

# npm generate

#cd ..

cp -R ./frontend/dist ./backend/frontend

cd ./backend

docker build -t pi-backend .

cd ..

cd ./miner

docker build -t pi-miner .
