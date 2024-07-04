from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config

def escribir_por_XPATH(xpath, texto):
    try:
        driver.find_element(By.XPATH, xpath).send_keys(texto)
        time.sleep(0.3)
    except Exception as e:
        print(f"No se pudo escribir en el elemento con el XPath {xpath}: {e}")

def clic_por_xpath(xpath, elemento=None):
    try:
        if elemento:
            elemento.find_element(By.XPATH, xpath).click()
        else:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        time.sleep(0.5)
    except Exception as e:
        print(f"No se pudo hacer clic en el elemento con el XPath {xpath}: {e}")
# Ejecución principal

# Configuración del driver
driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")
driver.maximize_window()
time.sleep(2)

# Login
escribir_por_XPATH("//input[@id='email']", config.EMAIL)
escribir_por_XPATH("//input[@id='pass']", config.PASS)
clic_por_xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/button[1]")
time.sleep(4)
clic_por_xpath("//span[contains(text(),'Guardado')]")

def realizar_acciones(descripcion, elemento_video):
    clic_por_xpath(".//span[contains(text(),'Añadir a una colección')]", elemento_video)
    time.sleep(0.3)
    
    if descripcion == "Descripcion A":
        # Acciones para Descripcion A
        clic_por_xpath("//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft'][normalize-space()='A']")

    elif descripcion == "Descripcion B":

        clic_por_xpath("//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft'][normalize-space()='B']")

    
    elif descripcion == "Descripcion C":

        clic_por_xpath("//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft'][normalize-space()='C']")

        
    elif descripcion == "Descripcion D":
        clic_por_xpath("//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft'][normalize-space()='D']")
        
    else:
        print(f"No se encontró una acción específica para: {descripcion}")  
    time.sleep(0.3)
    clic_por_xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/*[name()='svg'][1]")
    


# Lista de descripciones a buscar
descripciones = ["Descripcion A", "Descripcion B", "Descripcion C", "Descripcion D"]

# Buscar todos los elementos con la clase x1yztbdb
try:
    elementos_video = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x1yztbdb']"))
    )

    for elemento_video in elementos_video:
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento_video)
        time.sleep(1)

        texto_completo = elemento_video.text
        descripciones_encontradas = [desc for desc in descripciones if desc in texto_completo]
        
        for descripcion in descripciones_encontradas:
            print(f"Encontrada: {descripcion} en el elemento")
            realizar_acciones(descripcion, elemento_video)

except Exception as e:
    print(f"Error al procesar los elementos de video: {e}")

time.sleep(3)
driver.quit()