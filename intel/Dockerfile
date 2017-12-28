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

RUN apt-get update
RUN sudo apt-get  install -y xvfb x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps

ADD xvfb_init /etc/init.d/xvfb
RUN chmod a+x /etc/init.d/xvfb
ADD xvfb_daemon_run /usr/bin/xvfb-daemon-run
RUN chmod a+x /usr/bin/xvfb-daemon-run

RUN chmod +x chromedriver

EXPOSE 8350

CMD ["python3", "-u", "parsing.py"]
 
