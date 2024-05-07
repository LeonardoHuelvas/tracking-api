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
