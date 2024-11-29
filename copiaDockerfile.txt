FROM python:3.10-slim-bullseye

# Ajuste de hora
RUN apt-get update && apt-get install -y tzdata
ENV TZ="Chile/Continental"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instalar dependencias necesarias, incluyendo curl y gnupg
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    gconf-service \
    libasound2 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    unzip

# Instalar Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Copiar y instalar dependencias
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copiar el script de instalación de ChromeDriver y ejecutarlo
COPY install_chromedriver.py /app/install_chromedriver.py
RUN python /app/install_chromedriver.py

# Copiar la aplicación Flask
COPY app.py /app/app.py

# Copiar la carpeta procesos_web
COPY procesos_web /app/procesos_web

# Configurar variable de entorno DISPLAY para evitar crashes
ENV DISPLAY=:99

# Exponer el puerto para Flask
EXPOSE 5200

# Comando para ejecutar la aplicación Flask
CMD ["python", "/app/app.py"]
