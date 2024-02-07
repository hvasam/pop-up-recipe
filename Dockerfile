FROM python:3.10.12

WORKDIR /pop-up-recipe

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "http_server:app", "--host", "0.0.0.0", "--port", "8000"]