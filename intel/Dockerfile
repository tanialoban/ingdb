FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

USER root

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY . /usr/intel/

WORKDIR /usr/intel/

COPY chromedriver /usr/bin/
COPY chromedriver /usr/local/bin/
COPY chromedriver /usr/local/

USER admin
RUN chmod +x chromedriver

EXPOSE 8350

CMD ["python3", "parsing.py"]
 
