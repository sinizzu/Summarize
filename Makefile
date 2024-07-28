all: build run
stop: rm rmi
build:
	docker-compose up --build
run:
	docker run -it -d -p 3500:3500 --name subfastapi --env-file .env subfastapi
exec:
	docker exec -it subfastapi /bin/bash
logs:
	docker logs subfastapi
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi -f $$(docker images -q)
tag:
	docker tag subfastapi wjdguswn1203/subfastapi:latest
push:
	docker push wjdguswn1203/subfastapi:latest
pull:
	docker pull wjdguswn1203/subfastapi:latest