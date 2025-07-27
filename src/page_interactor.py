# page_interactor.py
import logging
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
# Necesario para usar By.ID en un string formateado
from selenium.webdriver.common.by import By

# Importar localizadores y configuraciones
import cfg.config as config
from dotenv import dotenv_values

cfg = {
    **dotenv_values("cfg/.env.secret")
}


class WebPageInteractor:
    """Realiza interacciones con la página web."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, config.DEFAULT_TIMEOUT)

    def _click_element(self, locator, retries=3, delay=1):
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                logging.info(f"Elemento clickeado: {locator}")
                return
            except ElementClickInterceptedException as e:
                logging.warning(
                    f"Intento {attempt + 1}/{retries}: Elemento click interceptado para {locator}. Reintentando en {delay}s. Error: {e}")
                time.sleep(delay)
            except TimeoutException:
                logging.error(
                    f"Timeout esperando para clickear elemento: {locator} después de {retries} intentos.")
                self.driver.save_screenshot(
                    f"error_click_timeout_{locator[1].replace(' ', '_')}.png")
                raise
        logging.error(
            f"No se pudo clickear el elemento {locator} después de {retries} intentos.")
        self.driver.save_screenshot(
            f"error_click_failed_{locator[1].replace(' ', '_')}.png")
        raise ElementClickInterceptedException(
            f"No se pudo clickear el elemento {locator} debido a intercepciones persistentes.")

    def _send_keys_to_element(self, locator, text):
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            logging.info(f"Texto '{text}' enviado a elemento: {locator}")
        except TimeoutException:
            logging.error(
                f"Timeout esperando por visibilidad del elemento para enviar texto: {locator}")
            self.driver.save_screenshot(
                f"error_send_keys_timeout_{locator[1].replace(' ', '_')}.png")
            raise
        except Exception as e:
            logging.error(f"Error al enviar texto a elemento {locator}: {e}")
            self.driver.save_screenshot(
                f"error_send_keys_{locator[1].replace(' ', '_')}.png")
            raise

    def _wait_for_element_visible(self, locator):
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator))
            logging.info(f"Elemento visible: {locator}")
            return element
        except TimeoutException:
            logging.error(
                f"Timeout esperando por visibilidad del elemento: {locator}")
            self.driver.save_screenshot(
                f"error_visibility_timeout_{locator[1].replace(' ', '_')}.png")
            raise
        except Exception as e:
            logging.error(
                f"Error esperando visibilidad del elemento {locator}: {e}")
            self.driver.save_screenshot(
                f"error_visibility_{locator[1].replace(' ', '_')}.png")
            raise

    def _wait_for_element_invisible(self, locator, timeout=None):
        custom_wait = WebDriverWait(
            self.driver, timeout) if timeout else self.wait
        try:
            custom_wait.until(EC.invisibility_of_element_located(locator))
            logging.info(f"Elemento ya no visible/presente: {locator}")
        except TimeoutException:
            # Esto no siempre es un error, el spinner podría no aparecer o desaparecer muy rápido.
            logging.warning(
                f"Timeout esperando que el elemento desaparezca: {locator}. Puede que ya no estuviera o el timeout sea corto.")
            # No relanzar la excepción aquí a menos que sea crítico.

    def login(self):
        logging.info(f"Navegando a la URL de login: {cfg['LOGIN_URL']}")
        self.driver.get(cfg['LOGIN_URL'])

        logging.info("Intentando seleccionar la empresa...")
        self._click_element(config.LOC_EMPRESA_DROPDOWN_CLICKABLE)

        # El contenedor de opciones de md-select suele ser 'select_container_X'
        # El ID del md-select era 'select_1', y en el HTML se veía aria-owns="select_container_2"
        # Por lo tanto, esperamos que 'select_container_2' se haga visible.
        self._wait_for_element_visible(
            (By.ID, "select_container_2"))  # Usar By.ID directamente

        xpath_string_formateado = config.LOC_EMPRESA_OPTION_XPATH_TPL.format(
            cfg['EMPRESA_TEXT_TO_SELECT'])
        empresa_option_locator = (By.XPATH, xpath_string_formateado)

        self._click_element(empresa_option_locator)
        logging.info(
            f"Empresa '{cfg['EMPRESA_TEXT_TO_SELECT']}' seleccionada.")

        self._send_keys_to_element(config.LOC_USERNAME_FIELD, cfg['USERNAME'])
        self._send_keys_to_element(config.LOC_PASSWORD_FIELD, cfg['PASSWORD'])
        self._click_element(config.LOC_LOGIN_BUTTON)
        logging.info("Botón 'Entrar' clickeado.")
        time.sleep(1)  # Pausa explícita solicitada
        logging.info("Pausa de 1 segundo después del login.")
        # Idealmente, esperar a un elemento de la siguiente página
        self._wait_for_element_visible(config.LOC_SIPS_MENU_LINK)

    def navigate_to_sips_section(self):
        logging.info("Navegando a la sección SIPS...")
        self._click_element(config.LOC_SIPS_MENU_LINK)
        self._wait_for_element_visible(config.LOC_CUPS_INPUT_FIELD)
        logging.info("Sección SIPS cargada.")

    def search_by_cups(self, cups_value):
        logging.info(f"Buscando CUPS: {cups_value}")
        self._send_keys_to_element(config.LOC_CUPS_INPUT_FIELD, cups_value)
        self._click_element(config.LOC_CONSULTAR_BUTTON)

        logging.info(
            "Esperando a que el spinner de carga desaparezca tras consulta...")
        self._wait_for_element_invisible(
            config.LOC_LOADING_SPINNER)  # Espera clave
        logging.info("Spinner de carga desaparecido.")

        self._wait_for_element_visible(config.LOC_RESULT_CHECKBOX)
        logging.info("Búsqueda de CUPS completada. Resultados visibles.")

    def select_result_and_download(self):
        logging.info("Seleccionando resultado y preparando descarga...")

        # Asegurarse de que no haya spinner antes de interactuar con el checkbox
        logging.info(
            "Verificando ausencia de spinner antes de clickear checkbox...")
        self._wait_for_element_invisible(
            config.LOC_LOADING_SPINNER, timeout=5)  # Timeout corto aquí

        # 1. Click en el checkbox
        try:
            # Usar EC.element_to_be_clickable es más robusto.
            # El método _click_element ya usa element_to_be_clickable.
            self._click_element(config.LOC_RESULT_CHECKBOX)
            logging.info("Checkbox de resultado clickeado.")
        except TimeoutException:
            logging.error(
                f"Timeout esperando que el checkbox {config.LOC_RESULT_CHECKBOX} sea clickeable.")
            self.driver.save_screenshot("error_checkbox_not_clickable.png")
            raise
        except Exception as e:  # Captura ElementClickInterceptedException u otras
            logging.error(
                f"No se pudo clickear el checkbox {config.LOC_RESULT_CHECKBOX}: {e}")
            self.driver.save_screenshot("error_checkbox_click.png")
            raise

        # 2. Click en el botón de descarga
        logging.info(
            "Esperando a que el spinner (si lo hubo) desaparezca antes de la descarga...")
        self._wait_for_element_invisible(
            config.LOC_LOADING_SPINNER)  # Espera clave

        try:
            # _click_element ya usa element_to_be_clickable
            self._click_element(config.LOC_DOWNLOAD_BUTTON)
            logging.info("Botón de descarga clickeado.")
        except TimeoutException:
            logging.error(
                "Timeout: El botón de descarga no se habilitó o no fue clickeable.")
            self.driver.save_screenshot(
                "error_download_button_not_enabled.png")
            btn_state = "No se pudo obtener estado"
            try:
                btn = self.driver.find_element(*config.LOC_DOWNLOAD_BUTTON)
                btn_state = btn.get_attribute('outerHTML')
            except:
                pass
            logging.debug(f"Estado del botón de descarga: {btn_state}")
            raise
        except Exception as e:  # Captura ElementClickInterceptedException u otras
            logging.error(
                f"Error al clickear botón de descarga {config.LOC_DOWNLOAD_BUTTON}: {e}")
            self.driver.save_screenshot("error_download_button_click.png")
            raise

        logging.info(
            f"Esperando {config.DEFAULT_TIMEOUT // 2} segundos para que la descarga se complete (aproximado)...")
        time.sleep(config.DEFAULT_TIMEOUT // 2)

        files = os.listdir(config.DOWNLOAD_DIR)
        if files:
            logging.info(
                f"Archivos encontrados en {config.DOWNLOAD_DIR}: {files}")
            # Podrías añadir lógica para verificar el archivo específico
        else:
            logging.warning(
                f"No se encontraron archivos en {config.DOWNLOAD_DIR} después de la descarga.")
