FROM python:3.10-slim

LABEL maintainer="modbus_simulation"

EXPOSE 502

COPY requirements.txt .
RUN python -m pip3 install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python","modbus_main.py"]