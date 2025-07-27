# === scraper.py ===
# Punto de entrada principal para ejecutar el scraper
# 1. Para ver el navegador en acción, cambia HEADLESS_MODE a False en cfg/config.py
##

import os
import time

import cfg.config as config
from src.browser_manager import HeadlessBrowserManager
from src.page_interactor import WebPageInteractor


class Scraper:
    """Handle el flujo completo de automatización."""

    def __init__(self, headless_mode):
        if not os.path.exists(config.DOWNLOAD_DIR):
            os.makedirs(config.DOWNLOAD_DIR)
            print(
                f"Directorio de descargas creado: {config.DOWNLOAD_DIR}")

        self.browser_manager = HeadlessBrowserManager(
            download_dir=config.DOWNLOAD_DIR,
            headless=headless_mode
        )
        self.driver = self.browser_manager.get_driver()
        self.interactor = WebPageInteractor(self.driver)

    def run_automation(self, cups_to_search=None):
        try:
            self.interactor.login()
            self.interactor.navigate_to_sips_section()
            self.interactor.search_by_cups(cups_to_search)
            self.interactor.select_result_and_download()
            print("Proceso de automatización completado exitosamente.")
        except Exception as e:
            print(
                f"Ocurrió un error durante la automatización: {e}")
            if self.driver:
                self.driver.save_screenshot("output/error_final_state.png")
                print(
                    "Se guardó una captura de pantalla: error_final_state.png")
        finally:
            if hasattr(self, 'browser_manager') and self.browser_manager:
                self.browser_manager.close_driver()
