FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY . /usr/intel/

COPY chromedriver /usr/local/lib/python3.5/
COPY chromedriver /usr/intel/
COPY chromedriver /usr/local/lib/
COPY chromedriver /usr/bin/
COPY chromedriver /usr/local/lib/python3.5/site-packages/selenium/webdriver/chrome/
COPY chromedriver /usr/local/bin/
COPY chromedriver /usr/local/lib/python3.5/site-packages/selenium/webdriver/common/
WORKDIR /usr/intel/

USER root

ENV CHROME_BIN /usr/bin/google-chrome

RUN chmod +x install.sh
RUN chmod +x chromedriver

EXPOSE 8350

CMD ["python3", "-u", "parsing.py"]
 
