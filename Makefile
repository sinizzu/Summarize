all: build run
stop: rm rmi
build:
	docker build -t subfastapi .
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