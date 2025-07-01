# 🌍 SISMOS_ETL - Pipeline ETL con Airflow + PostgreSQL + Streamlit

Este proyecto implementa un pipeline de datos que **extrae información de sismos desde la API del USGS**, la **transforma y la almacena en una base de datos PostgreSQL en Azure** utilizando Apache Airflow. Además, se proporciona una visualización interactiva mediante **Streamlit**.

---

## 📁 Estructura del Proyecto

```
SISMOS_ETL/
├── airflow/
│   ├── dags/
│   │   ├── earthquake_etl.py
│   │   ├── carga.py
│   │   └── extracción_transformacion.py
│   └── plugins/
│       └── .gitkeep
├── streamlit_app/
│   └── visualizar_streamlit.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Tecnologías utilizadas

- **Python 3.7**
- **Apache Airflow 2.5.1**
- **PostgreSQL (Azure)**
- **Streamlit**
- **Docker + Docker Compose**

---

## ⚙️ Configuración del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/sismos_etl.git
cd sismos_etl
```

### 2. Crear archivo `.env`

Copiar la plantilla y completarla con tus datos reales:

```bash
cp .env.example .env
```

### 3. Levantar los servicios con Docker

```bash
docker-compose up --build
```

Accedé a Airflow en: [http://localhost:8080](http://localhost:8080)  
Usuario: `admin` | Contraseña: `admin`

---

## 💾 Variables de entorno

El archivo `.env` contiene:

```env
# Conexión a la base de datos PostgreSQL en Azure
DATABASE_URL=postgresql+psycopg2://<usuario>:<contraseña>@<host>:5432/<database>
```

Este valor se usa tanto en Airflow como en la aplicación Streamlit.

---

## 🧩 DAG principal (`earthquake_etl`)

- Extrae los datos de sismos en tiempo real desde **USGS Earthquake API**
- Realiza transformaciones de limpieza y filtrado (por ejemplo, magnitud mínima)
- Carga los datos en la base **PostgreSQL (Azure)**
---

## 📊 Visualización con Streamlit

Para ver los sismos en una app web interactiva:

```bash
cd streamlit_app
streamlit run visualizar_streamlit.py
```
## 📄 Licencia

MIT © Fernando Pedernera

---

## 🤝 Contacto

📧 fernandogpg21@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/fgpedernera/).
