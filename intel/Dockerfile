FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY ../chromedriver /usr/intel
COPY . /usr/intel/
WORKDIR /usr/intel/

EXPOSE 8350

CMD ["python3", "-u", "parsing.py"]
 
