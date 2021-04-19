FROM python:3.8-buster

RUN mkdir __logger && \
    # install google chrome
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable && \
    # install chromedriver
    apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    pip install --upgrade pip

# set display port to avoid crash
ENV DISPLAY=:99

# install app
ADD dist /tmp/tvscraper-dist
RUN pip install /tmp/tvscraper-dist/*.whl
ENTRYPOINT ["python3", "-m", "tvscraper"]