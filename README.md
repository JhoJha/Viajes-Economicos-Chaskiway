# 🚌 Chaskiway: Recomendador de Viajes Económicos por el Perú

**Chaskiway** es una aplicación web desarrollada como proyecto para el curso de Lenguaje de Programación 2. Su objetivo es ayudar a los usuarios a planificar viajes interprovinciales desde Lima de manera inteligente, recomendando las mejores opciones en función de su presupuesto, preferencias de clima y calidad del servicio.

---

## 🎯 Objetivo del Proyecto

Desarrollar una aplicación web interactiva que integre y analice datos de múltiples fuentes para ofrecer recomendaciones de viaje personalizadas. El proyecto demuestra la aplicación de técnicas de web scraping, procesamiento de datos, creación de bases de datos y visualización de información en una solución de software completa y funcional.

### Objetivos Específicos
- **Recolectar** información de pasajes, clima e imágenes de tres fuentes distintas.
- **Integrar** los datos recolectados en una única base de datos centralizada.
- **Desarrollar** un algoritmo de recomendación simple basado en un sistema de puntuación.
- **Crear** un dashboard visual e interactivo con Streamlit para presentar los resultados al usuario.

---

## 🧱 Arquitectura y Flujo de Datos

El proyecto sigue un pipeline de datos claro y modular para garantizar la calidad y consistencia de la información.

```
[Fuente 1: RedBus] --(Scraper)--> [Datos Crudos: JSONs] --+
                                                          |
[Fuente 2: API Clima] --(Scraper)--> [Datos Crudos: CSV] ----> [main.py: Combinación] --> [Base de Datos SQLite] --> [Frontend: Streamlit]
                                                          |
[Fuente 3: API Imágenes] --(Scraper)--> [Datos Crudos: JSON] --+
```

1.  **Extracción (Scraping):** Tres scripts independientes se encargan de recolectar los datos de sus respectivas fuentes y guardarlos en la carpeta `data/raw/`.
2.  **Combinación y Carga (ETL):** El script `main.py` actúa como orquestador. Lee los tres conjuntos de datos crudos, los limpia y los combina usando la ciudad de destino como clave común. El resultado se carga en una base de datos SQLite en `data/processed/`.
3.  **Presentación (Frontend):** La aplicación `frontend/app.py` se conecta únicamente a la base de datos final para leer los datos ya procesados y presentarlos al usuario.

---

## 📚 Fuentes de Información

1.  **Portal RedBus:** Se utiliza para extraer información detallada de viajes (precios, horarios, empresas, ratings, asientos disponibles) mediante técnicas de web scraping.
2.  **API Meteorológica (Visual Crossing):** Provee datos históricos y de pronóstico del clima para cada ciudad de destino, permitiendo filtrar por preferencias climáticas.
3.  **API de Imágenes (Pixabay):** Suministra imágenes representativas de alta calidad para cada destino, enriqueciendo la experiencia visual de la aplicación.

---

## 🚀 Tecnologías Utilizadas

- **Lenguaje:** Python 3.11
- **Web Scraping:** `requests`, `beautifulsoup4` (si aplica)
- **Procesamiento de Datos:** `pandas`
- **Base de Datos:** `sqlite3`
- **Frontend:** `streamlit`
- **Control de Versiones:** Git y GitHub

---

## 👨‍💻 Equipo de Desarrollo

| Integrante | Usuario de GitHub | Rol en el Proyecto |
| :--- | :--- | :--- |
| **Jhon Jhayro Villegas Verde** | `JhoJha` | Backend, Scraper de RedBus y Base de Datos |
| **Jonnathan Jesús Pedraza Laboriano** | `jonnathan2023` | Backend, Scraper de Imágenes y Frontend |
| **David Ojeda Valdiviezo** | `20210842` | Backend, Scraper de Clima y Dashboard |

---

## Git Workflow: Estrategia de Ramas

Para asegurar una colaboración ordenada y eficiente, el proyecto utiliza un flujo de trabajo basado en ramas de funcionalidad (`feature branches`):

-   🌳 **`main`**: Rama principal. Contiene únicamente las versiones estables y funcionales del proyecto. Solo se fusiona desde `dev` cuando una versión ha sido probada y aprobada por el equipo.
-   🛠️ **`dev`**: Rama de desarrollo e integración. Es la rama donde se unen todos los avances. Antes de fusionar a `main`, todo debe funcionar correctamente en `dev`.
-   🚌 **`scraper-redbus`**: Rama dedicada exclusivamente al desarrollo del scraper de RedBus y la lógica de su base de datos. (Responsable: Jhon Villegas).
-   🌦️ **`scraper-clima`**: Rama para el desarrollo del conector a la API de clima. (Responsable: David Ojeda Valdiviezo).
-   🖼️ **`scraper-imagenes`**: Rama para el desarrollo del conector a la API de imágenes. (Responsable: Jonnathan Pedraza).
-   🖥️ **`dashboard`**: Rama dedicada al desarrollo de la interfaz de usuario y las visualizaciones en Streamlit.

El flujo de trabajo es: cada integrante trabaja en su rama asignada, y una vez que su funcionalidad está completa, crea un **Pull Request** hacia la rama `dev` para su revisión e integración.

---

## 📌 Estado Actual del Proyecto

🚧 **En Desarrollo.**

- [X] Creación de la estructura base del proyecto y repositorio.
- [X] Definición de la estrategia de ramas y flujo de trabajo en Git.
- [ ] Desarrollo de los scrapers individuales.
- [ ] Diseño del esquema de la base de datos.
- [ ] Implementación del pipeline de integración de datos.
- [ ] Desarrollo de la interfaz de usuario en Streamlit.

---

## 📞 Contacto

Para más información, contactar a: `20231515@lamolina.edu.pe`
