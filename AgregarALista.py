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

def clic_por_xpath(xpath):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        time.sleep(0.5)
    except Exception as e:
        print(f"No se pudo hacer clic en el elemento con el XPath {xpath}: {e}")

def guardar_en_lista(post, lista):
    try:
        boton_accion = post.find_element(By.XPATH, ".//div[@aria-label='Acciones para esta publicación']")
        boton_accion.click()
        time.sleep(1)
        
        # Verificar si el post ya está guardado
        elementos_guardado = driver.find_elements(By.XPATH, "//span[contains(text(), 'Cancelar vídeo')]")
        if elementos_guardado:
            print(f"El post ya está guardado. Cancelando la acción.")
            return True
        
        clic_por_xpath("//span[normalize-space()='Se añadirá a tus elementos guardados.']")
        time.sleep(1)
        
        clic_por_xpath(f"//span[normalize-space()='{lista}']")
        clic_por_xpath("//span[contains(text(),'Listo')]")
        print(f"Post guardado en la lista '{lista}'")
        return True
    except Exception as e:
        print(f"Error al guardar en la lista '{lista}': {e}")
        return False

def procesar_posts():
    posts = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1yztbdb')]")
    nuevos_procesados = 0
    posts_para_guardados = []
    for post in posts:
        try:
            if "processed" not in post.get_attribute("class"):
                texto_post = post.text.lower()
                listas_para_guardar = []
                
                if "descripcion a" in texto_post:
                    listas_para_guardar.append("A")
                if "descripcion b" in texto_post:
                    listas_para_guardar.append("B")
                if "descripcion c" in texto_post:
                    listas_para_guardar.append("C")
                if "descripcion d" in texto_post:
                    listas_para_guardar.append("D")
                
                if listas_para_guardar:
                    if guardar_en_lista(post, listas_para_guardar[0]):
                        if len(listas_para_guardar) > 1:
                            posts_para_guardados.append((post, listas_para_guardar[1:]))
                        driver.execute_script("arguments[0].setAttribute('class', arguments[0].getAttribute('class') + ' processed')", post)
                        nuevos_procesados += 1
                        print(f"Post procesado y guardado inicialmente en {listas_para_guardar[0]}")
        except Exception as e:
            print(f"Error al procesar post: {e}")
    
    print(f"Total de nuevos posts procesados: {nuevos_procesados}")
    return nuevos_procesados, posts_para_guardados

# Configuración del driver
driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")
driver.maximize_window()
time.sleep(2)

# Login
escribir_por_XPATH("//input[@id='email']", config.EMAIL)
escribir_por_XPATH("//input[@id='pass']", config.PASS)
clic_por_xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/button[1]")
time.sleep(7)

# Ir al perfil
clic_por_xpath("//span[contains(text(),'Maxi Smith')]")
time.sleep(5)

# Procesar posts
total_nuevos, posts_para_guardados = procesar_posts()

# Scroll para cargar más posts
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Procesar nuevamente para capturar nuevos posts
nuevos_adicionales, mas_posts_para_guardados = procesar_posts()
total_nuevos += nuevos_adicionales
posts_para_guardados.extend(mas_posts_para_guardados)

print(f"Total de nuevos posts procesados en esta ejecución: {total_nuevos}")

time.sleep(5)
driver.quit()