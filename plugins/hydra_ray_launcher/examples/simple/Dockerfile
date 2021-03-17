FROM python:3.8.8-slim

RUN apt-get update && apt-get install -y libc-dev gcc

RUN pip install hydra-core==1.1.0.dev4 hydra-ray-launcher==0.1.3 ray

WORKDIR /app

COPY . /app

CMD HYDRA_FULL_ERROR=1 python3 /app/my_app.py --multirun hydra/launcher=ray
