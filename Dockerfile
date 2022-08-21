FROM python:3.10
WORKDIR /server
RUN apk add --no-cache gcc musl-dev linux-headers
EXPOSE 8090
COPY . .
RUN $HOME/.poetry/bin/poetry export --dev -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
CMD ["python main.py", "run"]