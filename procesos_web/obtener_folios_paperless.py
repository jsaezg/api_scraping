import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
try:
    from procesos_web.codigos_series import series_codigos
except:
    from codigos_series import series_codigos

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')
#options.add_argument('--remote-debugging-port=9222')

documentos=dict(Guia_Despacho=52,
                Boleta=39,
                Factura=33,Factura_Exenta=34,Factura_Exportacion=110,
                Nota_Credito=61, Nota_Credito_Exportacion=112, 
                Nota_Debito=56 ,Nota_Debito_Exportacion=111)

def login_paperless():
    
    url_inicio = "http://130.1.1.228:8080/Facturacion/index.jsp"
    driver = webdriver.Chrome(options=options)
    driver.get(url_inicio)
    print(driver.title)

    # Localizar los campos de entrada
    rut_field = driver.find_element(By.ID, "txtRut")
    username_field = driver.find_element(By.ID, "txtLogin")
    password_field = driver.find_element(By.ID, "txtPasswd")

    # Ingresar los datos de login
    rut_field.send_keys("81105000-8")
    username_field.send_keys("adm_villalba")
    password_field.send_keys("abc123")

    # Enviar el formulario
    submit_button = driver.find_element(By.NAME, "imageField")
    submit_button.click()
    driver.save_screenshot('login0.png')
    return driver

#def lista_series_folios(tipo_documento="Factura"):
def lista_series_folios(documento="factura"):
    driver = login_paperless()
    driver.save_screenshot('login1.png')
    num_documento=series_codigos[documento]["codigo_documento"]
    url_folios=f"http://130.1.1.228:8080/Facturacion/parte5/folios/5cons_12foldetal.jsp?td={num_documento}"
    driver.get(url_folios)
    driver.save_screenshot('login2.png')
    rows_with_checkbox = driver.find_elements(By.XPATH, ".//tr[.//input[@type='checkbox' and @name='chkId']]")
    datos = []
    for index, row in enumerate(rows_with_checkbox):
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text for cell in cells]
        if len(data)==10:
            datos.append(data)
    driver.save_screenshot('login3.png')
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