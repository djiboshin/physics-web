FROM python:3

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y wkhtmltopdf

RUN cd svelte && npm install && npm run build

CMD ["python", "-m", "server"]
