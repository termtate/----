FROM python:3.10-slim

LABEL maintainer="snap7_simulation"

EXPOSE 102

COPY requirements.txt .
RUN python -m pip3 install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python","snap7_main.py"]