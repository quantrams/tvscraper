include config.mk
PHONY := clean image tests tests-docker

dist: clean
	poetry build

image: dist
	docker build --rm -t $(DOCKER_IMAGE) .

tests-docker: image 
	make -p ./downloads
	docker run --rm -it -v ${PWD}/downloads:/tmp/chrome_downloads \
		-v /dev/shm:/dev/shm --env-file .env $(DOCKER_IMAGE) \
		--url "https://www.tradingview.com/chart/BCEOOLCE/"

tests: tests-docker
	tox --

clean:
	rm -rf dist