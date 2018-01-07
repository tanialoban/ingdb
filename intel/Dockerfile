FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

USER root

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY . /usr/intel/

WORKDIR /usr/intel/

COPY geckodriver /usr/bin/
COPY geckodriver /usr/local/bin/
COPY geckodriver /usr/local/

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz

RUN chmod +x geckodriver

EXPOSE 8350

CMD ["python3", "parsing.py"]
 
