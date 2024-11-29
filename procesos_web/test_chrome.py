from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')

def login_intcomex():
    #url_inicio = "https://intcomexaccounts.b2clogin.com/intcomexaccounts.onmicrosoft.com/b2c_1a_signup_signin/oauth2/v2.0/authorize"
    url_inicio = "https://store.intcomex.com/es-XCL/AccountAjax/SignIn"
    driver = webdriver.Chrome(options=options)
    print("Init driver")
    driver.get(url_inicio)
    driver.save_screenshot('login0.png')
    print("Espera 10 segundos")
    driver.implicitly_wait(10)
    print("Pagina cargada")
    driver.save_screenshot('login1.png')
    # Localizar los campos de entrada
    username_field = driver.find_element(By.ID, "signInName")
    password_field = driver.find_element(By.ID, "password")

    # Ingresar los datos de login
    username_field.send_keys("evillena@getitsolutions.cl")
    password_field.send_keys("9127Elia*")
    driver.save_screenshot('login2.png')
    # Enviar el formulario presionando Enter
    #password_field.send_keys(Keys.RETURN)

    submit_button = driver.find_element(By.ID, "next")
    submit_button.click()
    driver.save_screenshot('login3.png')
    # Puedes agregar un tiempo de espera para permitir que la página cargue
    driver.implicitly_wait(10)

    # Verificar si el login fue exitoso (esto puede depender de la página)
    print(driver.title)
    driver.save_screenshot('login4.png')

    
    return driver