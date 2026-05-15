import streamlit as st
import grpc
import pandas as pd
from io import StringIO

import archivo_pb2
import archivo_pb2_grpc

DIRECCION_GRPC = 'localhost:50051'

def crear_cliente_grpc():
    # Ampliamos el límite de recepción del cliente a 50MB
    opciones_red = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024)
    ]
    canal = grpc.insecure_channel(DIRECCION_GRPC, options=opciones_red)
    return archivo_pb2_grpc.MotorAnaliticaStub(canal)

st.set_page_config(page_title="Dashboard Seguridad Nacional", layout="wide")
st.title("🛡️ Dashboard de Seguridad Nacional Ecuador")

# --- CONTROLES DE INTERACTIVIDAD Y FILTROS AVANZADOS ---
st.sidebar.header("🔍 Filtros de Tiempo")

# Filtros predeterminados
tipo_filtro = st.sidebar.radio(
    "Seleccione el modo de búsqueda:",
    ("Todo el histórico (2014-2025)", "Últimos 5 años (2021-2025)", "Año específico", "Rango personalizado")
)

# Lógica del filtro
if tipo_filtro == "Todo el histórico (2014-2025)":
    anio_inicio, anio_fin = 2014, 2025
    st.sidebar.info("Mostrando datos de 2014 a 2025")
elif tipo_filtro == "Últimos 5 años (2021-2025)":
    anio_inicio, anio_fin = 2021, 2025
    st.sidebar.info("Mostrando datos de 2021 a 2025")
elif tipo_filtro == "Año específico":
    anio_unico = st.sidebar.selectbox("Seleccione el año:", list(range(2014, 2026)), index=10)
    anio_inicio, anio_fin = anio_unico, anio_unico
else:
    anio_inicio, anio_fin = st.sidebar.slider(
        "Deslice para seleccionar el rango:",
        min_value=2014, max_value=2025, value=(2014, 2025)
    )

st.sidebar.divider()
variable_visualizar = st.sidebar.selectbox(
    "📊 Variable a graficar en frecuencia:",
    ("Provincia", "Tipo de Arma")
)

# Creamos el objeto de petición gRPC
filtro_rpc = archivo_pb2.FiltroAnios(anio_inicio=anio_inicio, anio_fin=anio_fin)
cliente = crear_cliente_grpc()

# --- MANEJO DE RED Y RENDERIZADO ---
try:
    # 1. Agregación Inicial (Tarjetas KPI)
    respuesta_agregacion = cliente.ObtenerAgregacionInicial(filtro_rpc)
    st.subheader(f"Resumen de Casos ({anio_inicio} - {anio_fin})")
    col1, col2, col3, col4 = st.columns(4)
    
    dict_agregacion = {item.categoria: item.cantidad for item in respuesta_agregacion.datos}
    
    col1.metric("Homicidios", f'{dict_agregacion.get("HOMICIDIO", 0):,}')
    col2.metric("Asesinatos", f'{dict_agregacion.get("ASESINATO", 0):,}')
    col3.metric("Sicariatos", f'{dict_agregacion.get("SICARIATO", 0):,}')
    col4.metric("Femicidios", f'{dict_agregacion.get("FEMICIDIO", 0):,}')

    st.divider()

    # 2. Resumen de Tabla (Dataframe completo)
    st.subheader("Base de Datos Procesada")
    respuesta_tabla = cliente.ObtenerResumenTabla(filtro_rpc)
    
    if respuesta_tabla.total_registros > 0:
        df_resumen = pd.read_json(StringIO(respuesta_tabla.json_dataframe))
        st.write(f"✅ **Total de registros encontrados:** {respuesta_tabla.total_registros:,}")
        # st.dataframe es súper eficiente y permite scroll en tablas de miles de filas
        st.dataframe(df_resumen, use_container_width=True, height=250)
    else:
        st.warning("No hay registros para este periodo.")

    st.divider()

    # 3. Gráficos Dinámicos
    st.subheader(f"Distribución de casos por {variable_visualizar}")
    if variable_visualizar == "Provincia":
        respuesta_frec = cliente.ObtenerFrecuenciaProvincia(filtro_rpc)
    else:
        respuesta_frec = cliente.ObtenerFrecuenciaArma(filtro_rpc)

    df_frecuencias = pd.DataFrame([
        {"Categoría": item.categoria, "Cantidad": item.cantidad} 
        for item in respuesta_frec.datos
    ])

    if not df_frecuencias.empty:
        # Ordenamos de mayor a menor para que el gráfico se vea profesional
        df_frecuencias = df_frecuencias.sort_values(by="Cantidad", ascending=False)
        col_graf_1, col_graf_2 = st.columns([2, 1]) # El gráfico toma el doble de espacio que la tabla
        
        with col_graf_1:
            st.bar_chart(data=df_frecuencias, x="Categoría", y="Cantidad", color="#ff4b4b")
        with col_graf_2:
            st.dataframe(df_frecuencias, hide_index=True, use_container_width=True)
    else:
        st.info("Gráfico no disponible por falta de datos en este rango.")

except grpc.RpcError as e:
    st.error(f"🚨 **Servicio no disponible.** Detalle técnico: {e.details()}")
except Exception as e:
    st.error(f"Error inesperado: {str(e)}")