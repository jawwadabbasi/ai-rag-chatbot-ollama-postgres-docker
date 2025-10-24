FROM python:3.11.9-alpine3.20

RUN apk update && apk upgrade && apk add bash

WORKDIR /var/www/html
COPY src/ .
COPY dev/settings.py .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python","main.py"]