FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

USER root

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY . /usr/intel/

WORKDIR /usr/intel/

COPY geckodriver /usr/intel/
COPY geckodriver /usr/bin/
COPY geckodriver /usr/local/bin/
COPY geckodriver /usr/local/

USER root
RUN sudo chmod +x geckodriver

EXPOSE 8350

CMD ["python3", "parsing.py"]
 
