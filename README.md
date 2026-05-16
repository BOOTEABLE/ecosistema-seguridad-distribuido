# 🛡️ Ecosistema Distribuido de Analítica para la Seguridad Nacional

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Pyro4](https://img.shields.io/badge/Pyro4-Distributed%20Objects-orange?style=for-the-badge)
![gRPC](https://img.shields.io/badge/gRPC-Protocol%20Buffers-00bfa5?style=for-the-badge&logo=grpc)
![Streamlit](https://img.shields.io/badge/Streamlit-Reactive%20Dashboard-ff4b4b?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Optimized%20Analytics-150458?style=for-the-badge&logo=pandas)

---

## 📌 Descripción General

**Ecosistema Distribuido de Analítica para la Seguridad Nacional** es una arquitectura distribuida de tres capas diseñada para procesar, filtrar y visualizar grandes volúmenes de datos estadísticos oficiales sobre homicidios intencionales en Ecuador entre los años **2014 y 2025**.

El proyecto implementa principios avanzados de:

- Sistemas distribuidos orientados a servicios
- Procesamiento desacoplado por microservicios
- Serialización eficiente mediante Protocol Buffers
- Tolerancia a fallos de red
- Optimización extrema de memoria RAM con Pandas
- Comunicación híbrida utilizando **Pyro4 + gRPC**
- Dashboards reactivos con Streamlit

El ecosistema está diseñado bajo una filosofía de **alto rendimiento**, **aislamiento de procesos** y **delegación eficiente de responsabilidades** entre capas.

---

# 🏛️ Arquitectura Distribuida de 3 Capas

El sistema está compuesto por tres nodos altamente desacoplados que interactúan mediante protocolos de red especializados.

---

## 1️⃣ Capa de Datos — Nodo Maestro (Pyro4)

📁 `nodo_maestro_pyro/`

La capa de datos funciona como un **motor de persistencia en memoria RAM**.

Es el único componente autorizado para interactuar directamente con el archivo físico `.xlsx` o `.csv`.

### 🔧 Responsabilidades

- Cargar datasets masivos usando Pandas
- Reducir el consumo de RAM
- Exponer datos procesados mediante Pyro4
- Mantener el aislamiento del almacenamiento

### ⚡ Optimización Extrema de Memoria

El nodo maestro implementa varias estrategias avanzadas:

- Extracción únicamente de columnas críticas:
  - `fecha_infraccion`
  - `tipo_muerte`
  - `provincia`
  - `arma`

- Conversión de cadenas repetitivas a tipos:
  ```python
  category
  ```

- Eliminación de fechas completas tras extraer únicamente el año

Estas técnicas permiten reducir drásticamente el uso de memoria incluso trabajando con datasets masivos.

### 🌐 Comunicación

El nodo se publica dinámicamente utilizando:

```bash
python -m Pyro4.naming
```

Esto evita exponer direcciones IP de forma insegura y permite descubrimiento automático de servicios.

---

## 2️⃣ Capa Lógica — Nodo Intermedio (gRPC)

📁 `nodo_logico_grpc/`

Esta capa actúa simultáneamente como:

- Cliente Pyro4
- Servidor gRPC

Es el núcleo matemático y lógico del ecosistema.

### 🔧 Responsabilidades

- Ejecutar lógica de negocio
- Realizar agregaciones estadísticas
- Ejecutar:
  ```python
  value_counts()
  ```
- Transformar tablas a JSON
- Serializar datos mediante Protocol Buffers

### 🧠 Motor Matemático

Toda la carga computacional pesada se ejecuta aquí para evitar saturar el dashboard visual.

### 🛡️ Tolerancia a Fallos

El nodo verifica activamente:

- Estado del Nodo Maestro
- Disponibilidad del canal Pyro4
- Errores de conectividad
- Excepciones remotas

Las excepciones son propagadas de forma controlada y segura.

### 🚀 Canal de Red Ampliado

El servidor gRPC utiliza un canal configurado hasta:

```text
50 MB
```

Esto permite transmitir grandes tablas serializadas sin fragmentación ni bloqueos.

---

## 3️⃣ Capa de Presentación — Dashboard Streamlit

📁 `dashboard_streamlit/`

Es la interfaz visual del ecosistema y funciona como cliente gRPC.

### 🔧 Responsabilidades

- Renderizar dashboards reactivos
- Mostrar métricas y KPIs
- Filtrar información temporalmente
- Visualizar gráficos dinámicos

### 📊 Funcionalidades

- KPIs:
  - Homicidios
  - Asesinatos
  - Sicariatos
  - Femicidios

- DataFrame completo en tiempo real
- Gráficos de barras dinámicos
- Sidebar con filtros avanzados

### ⚡ Manejo Inteligente en RAM

El dashboard utiliza:

```python
io.StringIO
```

para deserializar JSON masivos completamente en memoria, evitando errores relacionados con rutas físicas de archivos.

### 🛡️ Manejo Seguro de Excepciones

La interfaz captura errores como:

```python
grpc.RpcError
```

y muestra alertas amigables sin provocar el colapso de la aplicación.

---

# 🔄 Flujo de Comunicación del Ecosistema

```text
┌──────────────────────┐
│   Dashboard Streamlit│
│   (Cliente gRPC)     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Nodo Lógico gRPC     │
│ (Servidor + Cliente) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Nodo Maestro Pyro4   │
│ (Motor en RAM)       │
└──────────────────────┘
```

---

# 📁 Estructura del Proyecto

```text
ecosistema-seguridad-distribuido/
│
├── data/                                      # Ignorado en .gitignore
│   └── mdi_homicidiosintencionales_pm_2014_2025.xlsx
│
├── proto/
│   └── archivo.proto                          # Contrato fuente de verdad (gRPC)
│
├── nodo_maestro_pyro/
│   └── servidor_maestro.py                    # Capa 1: Persistencia y optimización RAM
│
├── nodo_logico_grpc/
│   ├── archivo_pb2.py                         # Generado por protoc
│   ├── archivo_pb2_grpc.py                    # Generado por protoc
│   └── servidor_grpc.py                       # Capa 2: Motor lógico y matemático
│
├── dashboard_streamlit/
│   ├── archivo_pb2.py                         # Generado por protoc
│   ├── archivo_pb2_grpc.py                    # Generado por protoc
│   └── app.py                                 # Capa 3: Dashboard interactivo
│
├── .gitignore
└── README.md
```

---

# ⚙️ Requisitos e Instalación

## 📥 Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/ecosistema-seguridad-distribuido.git

cd ecosistema-seguridad-distribuido
```

---

## 📦 Instalar Dependencias

```bash
pip install Pyro4 grpcio grpcio-tools pandas openpyxl streamlit
```

---

## 📂 Preparar Dataset

Crear la carpeta:

```text
data/
```

y colocar el archivo original:

```text
mdi_homicidiosintencionales_pm_2014_2025.xlsx
```

---

# 🚀 Guía de Ejecución

> ⚠️ IMPORTANTE:
> Debido a la naturaleza distribuida del ecosistema, el sistema requiere **4 terminales independientes** ejecutándose simultáneamente y en orden estricto.

---

## 🖥️ Terminal 1 — Name Server Pyro4

Inicia el registro de servicios distribuidos.

```bash
python -m Pyro4.naming
```

---

## 🖥️ Terminal 2 — Nodo Maestro Pyro4

Levanta el motor de persistencia y optimización RAM.

```bash
cd nodo_maestro_pyro

python servidor_maestro.py
```

---

## 🖥️ Terminal 3 — Nodo Lógico gRPC

Inicia el puente matemático intermedio.

```bash
cd nodo_logico_grpc

python servidor_grpc.py
```

---

## 🖥️ Terminal 4 — Dashboard Streamlit

Levanta la interfaz visual interactiva.

```bash
cd dashboard_streamlit

streamlit run app.py
```

---

# 🧩 Contrato de Comunicación — Protocol Buffers

El sistema utiliza:

```text
archivo.proto
```

como contrato estricto de serialización entre servicios.

Beneficios:

- Comunicación tipada
- Baja latencia
- Payloads compactos
- Alta interoperabilidad
- Serialización binaria eficiente

---

# 🛡️ Ingeniería Aplicada

## ✅ Tolerancia a Fallos de Red

El ecosistema implementa mecanismos avanzados de resiliencia:

- Verificación activa de conexión Pyro4
- Manejo de excepciones remotas
- Captura segura de:
  ```python
  grpc.RpcError
  ```
- Aislamiento entre capas
- Recuperación elegante ante caídas de nodos

El dashboard nunca colapsa abruptamente ante errores backend.

---

## ✅ Clean Code y Desacoplamiento

La arquitectura sigue principios sólidos de ingeniería:

- Separación estricta de responsabilidades
- Microservicios desacoplados
- Contratos definidos mediante `.proto`
- Código modular y mantenible
- Comunicación transparente entre procesos

---

## ✅ Optimización Extrema de RAM

El proyecto aplica técnicas reales de optimización para datasets masivos:

| Técnica | Beneficio |
|---|---|
| Selección parcial de columnas | Reduce lectura innecesaria |
| Conversión a `category` | Disminuye memoria en strings repetitivos |
| Extracción exclusiva del año | Reduce objetos datetime pesados |
| Procesamiento delegado | Evita saturar la capa visual |
| Serialización eficiente | Reduce overhead de red |

---

# 📈 Tecnologías Utilizadas

- Python 3
- Pandas
- Pyro4
- gRPC
- Protocol Buffers
- Streamlit
- OpenPyXL

---

# 🎯 Objetivo Técnico del Proyecto

Este proyecto fue diseñado para demostrar competencias avanzadas en:

- Arquitecturas distribuidas
- Procesamiento masivo de datos
- Sistemas tolerantes a fallos
- Comunicación RPC
- Optimización de memoria
- Dashboards analíticos
- Ingeniería backend escalable

---

# 👨‍💻 Autores

David Alejandro Cruz Palacios
Emily Mabel Ortega Constante
Carlos José Pilatuña Roldan

Estudiantes de Ingenieria en Ciencias de la Computación - Universidad Politécnica Salesiana (UPS)

Proyecto desarrollado para analítica de datos en seguridad ciudadana y arquitecturas distribuidas orientadas a servicios.

Diseñado con enfoque profesional para portafolios de ingeniería de software, backend distribuido y ciencia de datos aplicada.
