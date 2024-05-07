# Package Tracker API

## Descripción
Este proyecto es una API construida con Flask para el seguimiento de paquetes. Permite a los usuarios obtener detalles del estado actual de su envío introduciendo el número de seguimiento a través de una interfaz web o directamente a través de la API.

## Funcionalidad
- **Página de Inicio:** Retorna una página HTML básica que puede ser personalizada para incluir un formulario de seguimiento.
- **Endpoint de Seguimiento:** Recibe números de seguimiento a través de solicitudes POST y utiliza Selenium para obtener datos de seguimiento del sitio web correspondiente.

## Tecnologías Utilizadas
- **Flask:** Framework web utilizado para construir la API.
- **Selenium:** Utilizado para automatizar la navegación en el sitio web de seguimiento y extraer la información necesaria.

## Instalación y Configuración
1. Clonar el repositorio:

git clone https://github.com/LeonardoHuelvas/tracking-api.git

pip install -r requirements.txt

3. Configurar el driver de Chrome:
- Asegúrate de que el `chromedriver` esté en la ruta especificada en el script o actualiza la ruta según corresponda.

## Uso
Para iniciar la API, ejecuta:


Esto iniciará un servidor local en `http://127.0.0.1:5000/`. Puedes acceder a la API mediante los siguientes endpoints:
- Accede a `http://127.0.0.1:5000/` desde tu navegador para ver la página de inicio.
- Envía un POST request a `http://127.0.0.1:5000/track` con un JSON que incluya un `trackingNumber`, por ejemplo:
  ```json
  {
      "trackingNumber": "ZIMUMER2451448"
  }

