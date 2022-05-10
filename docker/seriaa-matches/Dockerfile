FROM python:3.8

RUN mkdir -p /usr/src/seriaa-matches/

WORKDIR /usr/src/seriaa-matches/

COPY . /usr/src/seriaa-matches/

ENV MY_API_KEY="MY API_TOKEN"
ENV MY_AWS_KEY="MY_AWS_KEY_FROM_IAM"
ENV MY_AWS_SECRET_KEY="MY_AWS_SECRET_KEY_FROM_IAM"

RUN pip install -r requirements.txt

CMD ["python", "seriaa-matches.py"]