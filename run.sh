#! /bin/bash

export $(cat .env | xargs)
docker swarm init
docker-compose -f stack.yml build adapter

docker stack deploy -c stack.yml tema3
