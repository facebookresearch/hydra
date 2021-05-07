FROM python:3.8.8-slim

RUN apt-get update && apt-get install -y libc-dev gcc

RUN pip install hydra-core==1.1.0.dev6 hydra-ray-launcher==1.1.0.dev1 ray

WORKDIR /app

COPY . /app

CMD HYDRA_FULL_ERROR=1 python3 /app/my_app.py --multirun hydra/launcher=ray
