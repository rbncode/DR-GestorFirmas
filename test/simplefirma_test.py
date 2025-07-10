
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# Fixture para iniciar y cerrar el navegador
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# CP-01 - Login con credenciales válidas
def test_cp01_login_credenciales_validas(driver):
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "email").send_keys("usuario@valido.com")
    driver.find_element(By.ID, "password").send_keys("contrasenaSegura123")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    assert "dashboard" in driver.current_url

# CP-02 - Login con credenciales inválidas
def test_cp02_login_credenciales_invalidas(driver):
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "email").send_keys("usuario@valido.com")
    driver.find_element(By.ID, "password").send_keys("incorrecta")
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "Usuario o contraseña inválida" in error

# CP-03 - Login con usuario inválido y contraseña válida
def test_cp03_login_usuario_invalido(driver):
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "email").send_keys("usuario@falso.com")
    driver.find_element(By.ID, "password").send_keys("contrasenaSegura123")
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "Usuario o contraseña inválida" in error

# CP-04 - Validación contra base de datos
def test_cp04_validacion_db(driver):
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "email").send_keys("usuario@valido.com")
    driver.find_element(By.ID, "password").send_keys("contrasenaSegura123")
    driver.find_element(By.ID, "login-button").click()
    assert "dashboard" in driver.current_url

# CP-05 - Validación usuario inexistente
def test_cp05_usuario_inexistente(driver):
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "email").send_keys("noexiste@correo.com")
    driver.find_element(By.ID, "password").send_keys("cualquiera")
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "Usuario no existente" in error

# CP-06 - Subir archivo PDF válido a Firebase
def test_cp06_subir_pdf_valido(driver):
    driver.get("http://localhost:8080/upload")
    driver.find_element(By.ID, "file-upload").send_keys("/ruta/a/documento.pdf")
    driver.find_element(By.ID, "upload-button").click()
    url = driver.find_element(By.ID, "archivo-url").get_attribute("href")
    assert "firebasestorage.googleapis.com" in url
    response = requests.head(url)
    assert response.status_code == 200

# CP-07 - Subir archivo inválido (exe)
def test_cp07_subir_archivo_invalido(driver):
    driver.get("http://localhost:8080/upload")
    driver.find_element(By.ID, "file-upload").send_keys("/ruta/a/archivo.exe")
    driver.find_element(By.ID, "upload-button").click()
    error = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "Formato no permitido" in error

# CP-08 - Verificar almacenamiento en nube
def test_cp08_verificar_almacenamiento(driver):
    driver.get("http://localhost:8080/upload")
    driver.find_element(By.ID, "file-upload").send_keys("/ruta/a/documento.pdf")
    driver.find_element(By.ID, "upload-button").click()
    url = driver.find_element(By.ID, "archivo-url").get_attribute("href")
    assert "firebasestorage.googleapis.com" in url
    response = requests.head(url)
    assert response.status_code == 200

# CP-09 - Ver estado intermedio
def test_cp09_estado_pendiente(driver):
    driver.get("http://localhost:8080/documentos")
    estado = driver.find_element(By.ID, "estado-doc-1").text
    assert estado == "Pendiente de firma"

# CP-10 - Ver estado firmado
def test_cp10_estado_firmado(driver):
    driver.get("http://localhost:8080/documentos")
    estado = driver.find_element(By.ID, "estado-doc-2").text
    assert estado == "Firmado"

# CP-11 - Firma válida
def test_cp11_firma_valida(driver):
    driver.get("http://localhost:8080/documento/firmar/123")
    driver.find_element(By.ID, "firmar-button").click()
    estado = driver.find_element(By.ID, "estado").text
    assert estado == "Firmado"

# CP-12 - Firma y trazabilidad
def test_cp12_trazabilidad(driver):
    driver.get("http://localhost:8080/documento/123/historial")
    historial = driver.find_element(By.ID, "historial").text
    assert "Firmado por Supervisor" in historial

# CP-13 - Rechazo con comentario
def test_cp13_rechazo_con_comentario(driver):
    driver.get("http://localhost:8080/documento/revisar/123")
    driver.find_element(By.ID, "comentario").send_keys("Documento incorrecto")
    driver.find_element(By.ID, "rechazar-button").click()
    estado = driver.find_element(By.ID, "estado").text
    assert estado == "Rechazado"

# CP-14 - Aprobación final
def test_cp14_aprobacion_final(driver):
    driver.get("http://localhost:8080/documento/aprobar/123")
    driver.find_element(By.ID, "aprobar-button").click()
    estado = driver.find_element(By.ID, "estado").text
    assert estado == "Aprobado"

# CP-15 - Flujo completo
def test_cp15_flujo_completo(driver):
    driver.get("http://localhost:8080/dashboard")
    assert "Aprobado" in driver.find_element(By.ID, "estado-final-doc").text

# CP-16 - Acceder a historial completo
def test_cp16_historial_completo(driver):
    driver.get("http://localhost:8080/historial")
    assert "Documentos firmados" in driver.page_source

# CP-17 - Búsqueda por fecha
def test_cp17_busqueda_fecha(driver):
    driver.get("http://localhost:8080/documentos")
    driver.find_element(By.ID, "fecha-inicio").send_keys("2025-06-01")
    driver.find_element(By.ID, "fecha-fin").send_keys("2025-06-05")
    driver.find_element(By.ID, "buscar-button").click()
    assert "Resultados para rango de fechas" in driver.page_source

# CP-18 - Filtro por estado y usuario
def test_cp18_filtro_estado_usuario(driver):
    driver.get("http://localhost:8080/documentos")
    driver.find_element(By.ID, "estado-select").send_keys("Pendiente")
    driver.find_element(By.ID, "usuario-input").send_keys("usuariox")
    driver.find_element(By.ID, "buscar-button").click()
    assert "usuariox" in driver.page_source

# CP-19 - Validar hash y firma
def test_cp19_hash_y_firma(driver):
    driver.get("http://localhost:8080/documento/firmado/123")
    assert "Hash válido" in driver.page_source

# CP-20 - Verificar acceso al archivo
def test_cp20_verificar_descarga(driver):
    driver.get("http://localhost:8080/documento/descargar/123")
    assert "Descargando documento firmado" in driver.page_source

# CP-21 - Registro de usuarios
def test_cp21_registro_valido(driver):
    driver.get("http://localhost:8080/registro")
    driver.find_element(By.ID, "nombre").send_keys("Nuevo Usuario")
    driver.find_element(By.ID, "email").send_keys("nuevo@correo.com")
    driver.find_element(By.ID, "password").send_keys("seguro123")
    driver.find_element(By.ID, "rol").send_keys("Empleado")
    driver.find_element(By.ID, "crear-button").click()
    assert "Usuario creado con éxito" in driver.page_source
