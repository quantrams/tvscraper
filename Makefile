include config.mk
PHONY := clean image tests tests-docker

dist: clean
	poetry build

image: dist
	docker build --rm -t $(DOCKER_IMAGE) .

tests-docker: image .env
	docker run --rm -it --env-file .env $(DOCKER_IMAGE) \
		-t AAPL -f Day -s 2021-03-01 -e 2021-04-01

tests: tests-docker
	tox --

clean:
	rm -rf dist