🛡️ Ecosistema Distribuido de Analítica para la Seguridad Nacional

Este proyecto es una Arquitectura Distribuida de Tres Capas diseñada para procesar, filtrar y visualizar grandes volúmenes de datos estadísticos oficiales sobre homicidios intencionales en Ecuador (2014-2025).

A través del uso de múltiples protocolos de comunicación en red (Pyro4 y gRPC) y optimización extrema de memoria con Pandas, este ecosistema demuestra principios avanzados de sistemas distribuidos, incluyendo tolerancia a fallos, aislamiento de procesos y serialización eficiente de datos.

🏛️ Arquitectura del Sistema

El ecosistema está dividido en 3 nodos o microservicios altamente desacoplados, los cuales operan en conjunto a través de canales de red:

1. Capa de Datos (Nodo Maestro - Pyro4)

Ubicado en nodo_maestro_pyro/. Es el único componente que tiene contacto con el archivo físico en el disco (.xlsx o .csv).

Función: Actúa como motor de base de datos en memoria (RAM).

Optimización: Carga exclusivamente las columnas necesarias y transforma cadenas de texto repetitivas en tipos category, reduciendo el uso de RAM drásticamente.

Protocolo: Utiliza el Nombre de Servicio (Name Server) de Pyro4 (pyro4-ns) para publicarse en la red sin revelar IPs de manera insegura.

2. Capa Lógica (Nodo Intermedio - gRPC)

Ubicado en nodo_logico_grpc/. Opera como cliente de Pyro4 y como servidor gRPC simultáneamente.

Función: Ejecuta la lógica de negocios, los conteos de frecuencia (value_counts()) y las agregaciones matemáticas para no delegar el trabajo pesado a la vista.

Tolerancia a fallos: Verifica activamente el estado de conexión del Nodo Maestro y maneja elegantemente las caídas de red, propagando excepciones seguras.

Red Ampliada: Cuenta con un canal configurado de 50MB de capacidad para soportar la transmisión masiva de tablas pesadas de manera fluida.

3. Capa de Presentación (Dashboard - Streamlit)

Ubicado en dashboard_streamlit/. Es la interfaz visual con el usuario.

Función: Genera la interfaz de controles avanzados y renderiza tableros de manera reactiva usando métricas y gráficos.

Manejo en RAM: Utiliza la librería io.StringIO para deserializar las enormes tablas convertidas en JSON sin obligar a Pandas a buscar archivos en el disco.

📁 Estructura del Proyecto

ecosistema-seguridad-distribuido/
│
├── data/                                      # [NO SUBIR AL REPO, ignorada en .gitignore]
│   └── mdi_homicidiosintencionales_pm_2014_2025.xlsx  
│
├── proto/
│   └── archivo.proto                          # Contrato fuente de verdad (gRPC)
│
├── nodo_maestro_pyro/
│   └── servidor_maestro.py                    # Capa 1: Gestión y optimización de base de datos
│
├── nodo_logico_grpc/
│   ├── archivo_pb2.py                         # Generado por el compilador protoc
│   ├── archivo_pb2_grpc.py                    # Generado por el compilador protoc
│   └── servidor_grpc.py                       # Capa 2: Motor matemático intermedio
│
├── dashboard_streamlit/
│   ├── archivo_pb2.py                         # Generado por el compilador protoc
│   ├── archivo_pb2_grpc.py                    # Generado por el compilador protoc
│   └── app.py                                 # Capa 3: Cliente Streamlit
│
├── .gitignore
└── README.md


🛠️ Requisitos e Instalación

Clona el repositorio:

git clone [https://github.com/TU_USUARIO/ecosistema-seguridad-distribuido.git](https://github.com/TU_USUARIO/ecosistema-seguridad-distribuido.git)
cd ecosistema-seguridad-distribuido


Instala las dependencias necesarias:

pip install Pyro4 grpcio grpcio-tools pandas openpyxl streamlit


Coloca el archivo original de datos en su lugar:
Crea la carpeta data/ en la raíz del proyecto y copia allí tu archivo Excel con el nombre: mdi_homicidiosintencionales_pm_2014_2025.xlsx.

🚀 Guía de Ejecución

Debido a su naturaleza distribuida, el sistema requiere levantar sus servicios de manera secuencial en terminales independientes.

Terminal 1 (Name Server de Pyro4)
Inicia el registro de nombres donde se reportará el maestro.

python -m Pyro4.naming


Terminal 2 (Nodo Maestro)
Levanta el motor de persistencia.

cd nodo_maestro_pyro
python servidor_maestro.py


Terminal 3 (Nodo Lógico gRPC)
Inicia el puente intermedio de cálculo.

cd nodo_logico_grpc
python servidor_grpc.py


Terminal 4 (Cliente Visual - Streamlit)
Inicia la vista interactiva para el usuario.

cd dashboard_streamlit
streamlit run app.py


💡 Manejo de Errores y Tolerancia a Fallos

Este proyecto cumple con los lineamientos de Clean Code e integra excepciones controladas. Si alguno de los nodos backend falla, el Dashboard no colapsará abruptamente; capturará los errores (como grpc.RpcError) y mostrará una alerta segura informando al usuario sobre la indisponibilidad del servicio.

Desarrollado para analítica de datos en Seguridad Ciudadana y arquitecturas distribuidas orientadas a servicios.
