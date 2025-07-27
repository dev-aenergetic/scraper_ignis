# Scraper Maxímetro Ignis

Este proyecto contiene una automatización para obtener los datos del maxímetro en formato Excel desde la página de Ignis.

## Características

-   **Automatización Completa**: Inicia sesión, navega hasta la sección correcta, busca por CUPS y descarga el fichero.
-   **Configurable**: Permite ejecutar el navegador en modo visible (`headless=False`) para depuración.
-   **Gestión de Dependencias**: Utiliza `uv` para un manejo de dependencias rápido y eficiente.

## Requisitos Previos

-   Python 3.13 o superior.
-   `uv` instalado en tu sistema. Puedes instalarlo con:
    ```bash
    pip install uv
    ```

## Configuración del Entorno

1.  **Clonar el Repositorio**
    ```bash
    git clone scraper_ignis
    cd scraper_ignis
    ```

2.  **Crear y Activar el Entorno Virtual**
    ```bash
    uv venv --python 3.13 .venv
    source .venv/bin/activate
    ```

3.  **Instalar Dependencias**
    ```bash
    uv pip install -r ./req/requirements.txt

    #On mac OS :
    brew install chromedriver
    xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver

    ```

4.  **Configurar Credenciales**
    Crea un fichero llamado `.env.secret` dentro de la carpeta `cfg/` con el siguiente contenido, reemplazando los valores de ejemplo:
    ```
    LOGIN_URL="https://pagina.de.ignis/login"
    EMPRESA_TEXT_TO_SELECT="Nombre de la Empresa"
    USERNAME="tu_usuario"
    PASSWORD="tu_contraseña"
    ```

## Uso

Para ejecutar el script, utilizar el siguiente comando, reemplazando `<numero_cups>` con el CUPS que deseas consultar:

```bash
python main.py '<numero_cups>'

$> python main "ESXXXXXXXXXXXXXXX"
WebDriver inicializado correctamente.
Proceso de automatización completado exitosamente.
WebDriver cerrado.
```

## Respuesta

Se descarga y se guarda en la carpeta output/ : 
- Un fichero .zip, de nombre : Tabla.zip
- Al descomprimir el fichero, encontramos un archivo Excel : Contenido-tabla.xls
- Del archivo nos interesan las siguientes columnas, que seran guardadas en la base de datos, asociadas al numero de Cups que fue ingresado.

Excel : Contenido-tabla.xls
  1. Fecha Lectura Inicial	
  2. Fecha Lectura Final
  3. P1 Maximetro	
  4. P2 Maximetro	
  5. P3 Maximetro	
  6. P4 Maximetro	
  7. P5 Maximetro	
  8. P6 Maximetro


## Estructura del Proyecto
scraper_ignis/
├── .venv/
├── cfg/
│   ├── .env.secret         # Credenciales (ignorado por Git)
│   └── config.py           # Configuraciones generales
├── req/
│   └── requirements.txt    # Dependencias
├── src/
│   ├── browser_manager.py  # Gestiona el WebDriver de Selenium
│   ├── page_interactor.py  # Lógica de interacción con la web
│   └── scraper.py          # Orquestador principal del scraper
├── main.py                 # Punto de entrada
└── readme.md

