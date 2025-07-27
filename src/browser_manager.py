# browser_manager.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class HeadlessBrowserManager:
    """Gestiona la creación y cierre del WebDriver."""

    def __init__(self, download_dir, headless=True):
        self.download_dir = download_dir
        self.headless = headless
        self.driver = None
        self._setup_driver()

    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Suprimir logs excesivos de DevTools
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])  # Suprimir logs de DevTools

        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        try:
            # Inicializar el WebDriver con ChromeDriverManager
            service = ChromeService('/opt/homebrew/bin/chromedriver')
            self.driver = webdriver.Chrome(
                service=service, options=chrome_options)

            # service = ChromeService(ChromeDriverManager().install())
            print("WebDriver inicializado correctamente.")
        except Exception as e:
            print(f"Error al inicializar WebDriver: {e}")
            raise

    def get_driver(self):
        if not self.driver:
            self._setup_driver()
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            print("WebDriver cerrado.")
