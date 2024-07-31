all: build run
stop: rm rmi
build:
	docker-compose up --build
run:
	docker run -it -d -p 3500:3500 --name summarize --env-file .env summarize
exec:
	docker exec -it summarize /bin/bash
logs:
	docker logs summarize
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi -f $$(docker images -q)
tag:
	docker tag summarize wjdguswn1203/summarize:latest
push:
	docker push wjdguswn1203/summarize:latest
pull:
	docker pull wjdguswn1203/summarize:latest