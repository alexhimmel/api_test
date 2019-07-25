FROM python:3.7.3-stretch

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

CMD [ "python", "--version" ]

