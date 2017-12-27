FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY . /usr/intel/

COPY chromedriver /usr/local/lib/python3.5/
COPY chromedriver /usr/intel/
COPY chromedriver /usr/bin/
COPY chromedriver /usr/local/lib/python3.5/site-packages/selenium/webdriver/chrome/
COPY chromedriver /usr/local/bin/
COPY chromedriver /usr/local/lib/python3.5/site-packages/selenium/webdriver/common/
WORKDIR /usr/intel/

RUN \
    apt-get update && apt-get install -y unzip && \
    LATEST_CHROMEDRIVER_VERSION=$(wget -qO- http://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    mkdir -p /opt/chromedriver-$LATEST_CHROMEDRIVER_VERSION && \
    wget https://chromedriver.storage.googleapis.com/${LATEST_CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$LATEST_CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$LATEST_CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$LATEST_CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver && \
    apt-get purge --auto-remove -y unzip && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Restore base image's user (run Chrome non-privileged)
USER chrome

EXPOSE 8350

CMD ["python3", "-u", "parsing.py"]
 
