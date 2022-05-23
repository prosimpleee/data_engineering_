FROM python:3.8

RUN mkdir -p /usr/src/hello/

WORKDIR /usr/src/hello/

COPY . /usr/src/hello/

RUN pip install pandas

CMD ["python", "hello.py"] 
