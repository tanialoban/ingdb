FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY chromedriver /usr/intel
COPY . /usr/intel/
WORKDIR /usr/intel/

RUN echo “deb http://ppa.launchpad.net/mozillateam/firefox-next/ubuntu trusty main” > /etc/apt/sources.list.d//mozillateam-firefox-next-trusty.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE49EC21
RUN apt-get update
RUN apt-get install -y firefox xvfb python-pip
RUN pip install selenium
RUN mkdir -p /root/selenium_wd_tests
ADD sel_wd_new_user.py /root/selenium_wd_tests
ADD xvfb.init /etc/init.d/xvfb
RUN chmod +x /etc/init.d/xvfb
RUN update-rc.d xvfb defaults
CMD (service xvfb start; export DISPLAY=:10; python /root/selenium_wd_tests/sel_wd_new_user.py)

EXPOSE 8350

CMD ["python3", "-u", "parsing.py"]
 
