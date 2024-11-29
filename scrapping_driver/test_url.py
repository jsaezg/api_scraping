#import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')
#options.add_argument('--remote-debugging-port=9222')

def get_web(url='https://www.emol.com'):
    # Inicializar el navegador
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navegar a la URL
        driver.get(url=url)
        
        # Obtener el título de la página
        title = driver.title
        
        # Tomar una captura de pantalla
        screenshot_path = 'screenshot.png'
        driver.save_screenshot(screenshot_path)
        
        # Codificar la imagen en Base64
        with open(screenshot_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Generar el HTML con el título y la imagen
        html_content = f"""
        <html>
        <head>
            <title>Resultado</title>
        </head>
        <body>
            <h1>{title}</h1>
            <img src="data:image/png;base64,{encoded_image}" alt="Screenshot">
        </body>
        </html>
        """
        return html_content

    except Exception as e:
        # Manejo de errores
        return f"<html><body><h1>Error: {str(e)}</h1></body></html>"

    finally:
        # Cerrar el navegador
        driver.quit()
