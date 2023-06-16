FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install requirements.txt

WORKDIR /app

COPY  ["predict.py", "lin_reg.bin","./"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]