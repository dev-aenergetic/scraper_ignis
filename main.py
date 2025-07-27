# === main.py ===
##
import cfg.config as config
import sys
from src.scraper import Scraper


def execute():
    if len(sys.argv) != 2:
        print("Ayuda de uso: python main.py '<cups_number>'")
        return

    # Obtener la informacion del maximetro del CUPS
    manager = Scraper(headless_mode=config.HEADLESS_MODE)
    manager.run_automation(cups_to_search=sys.argv[1])


# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    execute()
