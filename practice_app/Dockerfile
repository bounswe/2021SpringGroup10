FROM python:3.9.5-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["flask"]

CMD ["run", "--host=0.0.0.0"]