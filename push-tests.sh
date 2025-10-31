#! /bin/bash
IMAGE_NAME=nbank-test
DOCKER_USERNAME=andreykulikov68
DOCKER_TOKEN="dckr_pat_GTz2GKTG0gJInOK1bWgwG9C8b4k"
TAG=latest

docker build -t $IMAGE_NAME .

echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker tag $IMAGE_NAME $DOCKER_USERNAME/$IMAGE_NAME:$TAG

docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG



