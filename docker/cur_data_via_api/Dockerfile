FROM python:3.8


RUN mkdir -p /usr/src/cur_data_via_api/

WORKDIR /usr/src/cur_data_via_api/

COPY . /usr/src/cur_data_via_api/

RUN pip install -r requirements.txt

CMD ["python", "extract_data_via_api.py"]