FROM python:3.10
EXPOSE 8080
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install $(spacy info en_core_web_sm --url)
COPY . .
CMD ["uvicorn", "evidence_api:app", "--host", "0.0.0.0", "--port", "80"]