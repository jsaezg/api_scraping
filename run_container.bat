@echo off

set "CURRENT_DIR=%cd%"

:: Correr imagen
docker run -p 5200:5200 ^
    -v "%CURRENT_DIR%:/app" ^
    -e PORT=5200 ^
    flask-app


:: Construir imagen
:: docker build -t flask-app .

:: Reconstruir imagen
:: docker build -t flask-app .

:: Checkear imagen
:: docker images
