FROM python:3.5.2-alpine

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

RUN mkdir /usr/intel/
COPY chromedriver /usr/local/lib/python3.5/
COPY . /usr/intel/

sudo apt-get install chromium-browser

WORKDIR /usr/intel/
EXPOSE 8350

CMD ["python3", "-u", "parsing.py"]
 
