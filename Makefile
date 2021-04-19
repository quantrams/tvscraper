include config.mk
PHONY := clean image tests tests-docker

dist: clean
	poetry build

image: dist
	docker build --rm -t $(DOCKER_IMAGE) .

tests-docker: image 
	docker run --rm -it -v /dev/shm:/dev/shm $(DOCKER_IMAGE) 

tests: tests-docker
	tox --

clean:
	rm -rf dist