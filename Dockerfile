FROM python:3.10.2

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ADD . /usr/src/app/
RUN pip3 install --no-cache-dir -r req.txt

ENV TZ=Europe/Moscow

EXPOSE 5000

CMD ["python", "app1.py"]