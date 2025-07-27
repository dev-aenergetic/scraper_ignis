    # === config.py ===
    # Can be committed to version control.
    # ---

    import os
    from selenium.webdriver.common.by import By

    # --- Configuraciones Generales ---
    DOWNLOAD_DIR = os.path.join(os.getcwd(), "output")
    # Timeout en segundos para esperar a que los elementos aparezcan
    DEFAULT_TIMEOUT = 20
    # Modo headless, False para ver el navegador
    HEADLESS_MODE = True

    # --- Localizadores de Elementos ---

    # Página de Login
    LOC_EMPRESA_DROPDOWN_CLICKABLE = (By.ID, "select_1")
    LOC_EMPRESA_OPTION_XPATH_TPL = "//div[@id='select_container_2']//md-option[normalize-space(.)='{}']"
    LOC_USERNAME_FIELD = (By.NAME, "usuario")
    LOC_PASSWORD_FIELD = (By.NAME, "password")
    LOC_LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Entrar']")

    # Menú Principal (después del login)
    LOC_SIPS_MENU_LINK = (
        By.XPATH, "//a[contains(@href, '#/sips') and .//span[normalize-space()='SIPS']]")

    # Página SIPS
    LOC_CUPS_INPUT_FIELD = (By.XPATH, "//input[@ng-model='Cups']")
    LOC_CONSULTAR_BUTTON = (
        By.XPATH, "//button[span[normalize-space()='Consultar']]")
    LOC_LOADING_SPINNER = (By.ID, "cover-spin")  # Para el overlay de carga

    # El checkbox es <md-checkbox ...> <div class="md-container ..."> <div class="md-icon"></div> </div> </md-checkbox>
    # Seleccionamos el div.md-icon dentro del primer md-checkbox
    # LOC_RESULT_CHECKBOX = (By.XPATH, "(//md-checkbox//div[@class='md-icon'])[1]")
    LOC_RESULT_CHECKBOX = (
        By.XPATH, "(//md-checkbox/div[contains(@class, 'md-container')])[1]")

    LOC_DOWNLOAD_BUTTON = (
        By.XPATH, "//button[i[contains(@class, 'fa-save') and @aria-label='Descargar consumos']]")
