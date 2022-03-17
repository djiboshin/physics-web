FROM python:3

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && apt-get install -y nodejs
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb
RUN apt install fonts-liberation
RUN cd svelte && npm install && npm run build

CMD ["python", "-m", "server"]