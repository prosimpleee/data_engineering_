FROM python:3.8

RUN mkdir -p /usr/src/asos_products_data/

WORKDIR /usr/src/asos_products_data/

COPY . /usr/src/asos_products_data/

ENV MY_API_KEY="MY API_TOKEN"
ENV MY_AWS_KEY="MY_AWS_KEY_FROM_IAM"
ENV MY_AWS_SECRET_KEY="MY_AWS_SECRET_KEY_FROM_IAM"

RUN pip install -r requirements.txt

CMD ["python", "exc_products_asos.py"]