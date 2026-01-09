### Readme disponible en inglés y español | Readme available in English and Spanish.
### Desarrollado por Yariel Zamora del Cueto | Developed by Yariel Zamora del Cueto 
---
# 🎭 ImpostAPI | Backend Engine

> **"The API that lies to you."**

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**ImpostAPI** is a high-performance, asynchronous Mock API generator built with FastAPI and MongoDB. It allows developers to design and deploy custom JSON endpoints in seconds, streamlining the workflow when the real backend isn't available yet.

---

## 🤔 Why this project?

**ImpostAPI** solves the classic "chicken and egg" problem in software development: **How does the Frontend team advance if the Backend isn't ready yet?**

This project allows you to:
1.  **Unblock Frontend:** Create "contracts" (agreed-upon JSON responses) instantly to start building interfaces without dependencies.
2.  **Test the Hard Stuff (Unhappy Paths):** Simulate server errors (500), resources not found (404), or long timeouts in a controlled way.
3.  **Rapid Prototyping:** Ideal for Hackathons or demos where you need a functional API without writing complex business logic.

## 🎯 Who is this for?

- **Frontend Developers:** Who need immediate data to work on their components.
- **QA Engineers:** Who require deterministic test scenarios for their automated tests.
- **Fullstack Developers:** Who want to validate an architecture idea before coding the final backend.
- **Students & Teachers:** To practice consuming REST APIs in a controlled environment.

---

## ⚡ Key Features

- **🚀 Native Asynchronous Core:** Built with **FastAPI** and the modern **PyMongo (Async)** driver for non-blocking operations.
- **🔀 Dynamic "Catch-All" Routing:** An engine that intercepts any request under `/mock/{path}` and looks up the corresponding configuration in the database.
- **⏱️ Network Simulation:** Configurable latency per endpoint to test loading states and skeletons on the client side.
- **🛡️ Contract Testing:** Define custom JSON responses and Status Codes (200, 201, 400, 500).
- **💎 Pydantic v2:** Robust data validation using the latest industry standards.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** MongoDB (via native PyMongo Async)
- **Validation:** Pydantic v2
- **Environment:** Python 3.10+
- **Server:** Uvicorn (ASGI)

---

## 🚀 Installation and Usage

### Prerequisites
- Python 3.10+
- MongoDB Instance (Local or Atlas)

### 1. Clone the repository
```bash
git clone https://github.com/YarielZC/impostapi-back.git
cd impostapi-back
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Env Variables
Create a `.env` file in the root directory, using `.env.template` as a guide.

### 5. Run the Server
```bash
fastapi dev index.py
```
The API will be available at: `http://localhost:8000`

---

## 📚 API Documentation (Swagger)

FastAPI automatically generates interactive documentation. Visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
---

## 🤝 Contributions

Contributions are what make the open source community such an amazing place to learn and inspire.
1. **Fork** the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

---

## 📄 License

Distributed under the MIT License. See the `LICENSE` file for more information.
---
# 🎭 ImpostAPI | Backend Engine
> **"La API que te miente."**



![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

**ImpostAPI** es un generador de Mock APIs asíncrono y de alto rendimiento construido con FastAPI y MongoDB. Permite a los desarrolladores diseñar y desplegar endpoints JSON personalizados en segundos, agilizando el flujo de trabajo cuando el backend real aún no está disponible.

---

## 🤔 ¿Para qué sirve este proyecto?

**ImpostAPI** resuelve el problema clásico del "huevo y la gallina" en el desarrollo de software: **¿Cómo avanza el equipo de Frontend si el Backend aún no está listo?**

Este proyecto permite:
1.  **Desbloquear al Frontend:** Crea "contratos" (respuestas JSON acordadas) instantáneamente para empezar a maquetar interfaces sin dependencias.
2.  **Probar lo difícil (Unhappy Paths):** Simular errores de servidor (500), recursos no encontrados (404) o tiempos de espera largos de forma controlada.
3.  **Prototipado Rápido:** Ideal para Hackathons o demos donde necesitas una API funcional sin escribir lógica de negocio compleja.

## 🎯 ¿Para quién está dirigido?

- **Frontend Developers:** Que necesitan datos inmediatos para trabajar en sus componentes.
- **QA Engineers:** Que requieren escenarios de prueba deterministas para sus tests automatizados.
- **Fullstack Developers:** Que quieren validar una idea de arquitectura antes de codificar el backend final.
- **Estudiantes y Profesores:** Para practicar el consumo de APIs REST en un entorno controlado.

---

## ⚡ Características Principales

- **🚀 Núcleo Asíncrono Nativo:** Construido con **FastAPI** y el driver moderno de **PyMongo (Async)** para operaciones no bloqueantes.
- **🔀 Enrutamiento Dinámico "Catch-All":** Un motor que intercepta cualquier petición bajo `/mock/{path}` y busca la configuración correspondiente en la base de datos.
- **⏱️ Simulación de Red:** Latencia configurable por endpoint para probar estados de carga y skeletons en el cliente.
- **🛡️ Testing de Contratos:** Define respuestas JSON y Códigos de Estado (200, 201, 400, 500) personalizados.
- **💎 Pydantic v2:** Validación de datos robusta utilizando los últimos estándares de la industria.

---

## 🛠️ Stack Tecnológico

- **Framework:** FastAPI
- **Base de Datos:** MongoDB (vía PyMongo Async nativo)
- **Validación:** Pydantic v2
- **Entorno:** Python 3.10+
- **Servidor:** Uvicorn (ASGI)

---

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.10+
- Instancia de MongoDB (Local o Atlas)

### 1. Clonar el repositorio
```bash
git clone https://github.com/YarielZC/impostapi-back.git
cd impostapi-back
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Env
Crea un archivo `.env` en la raíz, guiarse por `.env.template`:

### 5. Ejecutar el Servidor
```bash
fastapi dev index.py
```
La API estará en: `http://localhost:8000`

---

## 📚 Documentación de la API (Swagger)

FastAPI genera documentación interactiva automáticamente. Visita:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
---


## 🤝 Contribuciones

Las contribuciones son lo que hacen a la comunidad de código abierto un lugar increíble para aprender e inspirar.
1. Haz un **Fork** del proyecto.
2. Crea tu rama de funcionalidad (`git checkout -b feature/MejoraIncreible`).
3. Haz **Commit** de tus cambios (`git commit -m 'Add some MejoraIncreible'`).
4. Haz **Push** a la rama (`git push origin feature/MejoraIncreible`).
5. Abre un **Pull Request**.

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver el archivo `LICENSE` para más información.
