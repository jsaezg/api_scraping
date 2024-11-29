import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def login_intcomex():
    #url_inicio = "https://intcomexaccounts.b2clogin.com/intcomexaccounts.onmicrosoft.com/b2c_1a_signup_signin/oauth2/v2.0/authorize"
    url_inicio = "https://store.intcomex.com/es-XCL/AccountAjax/SignIn"
    driver = webdriver.Chrome(options=options)
    print("Init driver")
    driver.get(url_inicio)
    print("Espera 10 segundos")
    driver.implicitly_wait(10)
    print("Pagina cargada")

    # Localizar los campos de entrada
    username_field = driver.find_element(By.ID, "signInName")
    password_field = driver.find_element(By.NAME, "passwd")

    # Ingresar los datos de login
    username_field.send_keys("evillena@getitsolutions.cl")
    password_field.send_keys("9127Elia*")

    # Enviar el formulario presionando Enter
    password_field.send_keys(Keys.RETURN)

    # Puedes agregar un tiempo de espera para permitir que la página cargue
    driver.implicitly_wait(10)

    # Verificar si el login fue exitoso (esto puede depender de la página)
    print(driver.title)

    return driver

#def lista_series_folios(tipo_documento="Factura"):
def lista_series_folios(documento="factura"):
    driver = login_paperless()
    num_documento=series_codigos[documento]["codigo_documento"]
    url_folios=f"http://130.1.1.228:8080/Facturacion/parte5/folios/5cons_12foldetal.jsp?td={num_documento}"
    driver.get(url_folios)
    rows_with_checkbox = driver.find_elements(By.XPATH, ".//tr[.//input[@type='checkbox' and @name='chkId']]")
    datos = []
    for index, row in enumerate(rows_with_checkbox):
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text for cell in cells]
        if len(data)==10:
            datos.append(data)
    driver.quit()
    # Definir columnas
    columnas = ["checkbox", "Id", "Fecha_Ingreso", "Folio_Inicial", "Folio_Final", "Total", "Fecha_SII", "Estado", "Asignación", "CAF"]    
    # Crear DataFrame
    datos = pd.DataFrame(datos, columns=columnas)
    datos.drop(columns=["checkbox", "Estado", "Asignación", "CAF"], inplace=True)
    # Convertir columnas a tipos de datos adecuados
    #datos["Tipo_Documento"]=tipo_documento
    datos["Id"] = datos["Id"].astype(int)
    datos["Folio_Inicial"] = datos["Folio_Inicial"].astype(int)
    datos["Folio_Final"] = datos["Folio_Final"].astype(int)
    datos["Total"] = datos["Total"].str.replace('.', '').astype(int)  # Eliminar el punto antes de convertir a int
    #datos["Fecha_Ingreso"] = pd.to_datetime(datos["Fecha_Ingreso"], format='%d-%m-%Y %H:%M')
    #datos["Fecha_SII"] = pd.to_datetime(datos["Fecha_SII"], format='%Y-%m-%d').dt.date
    return datos

#from obtener_folios_paperless import *