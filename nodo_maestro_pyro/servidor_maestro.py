import Pyro4
import pandas as pd
import os

RUTA_EXCEL = "../data/mdi_homicidiosintencionales_pm_2014_2025.xlsx"
RUTA_CSV = "../data/dataset_procesado.csv"

# Usamos los nombres EXACTOS del archivo original
COLUMNAS_UTILES = ['fecha_infraccion', 'tipo_muerte', 'provincia', 'arma']

@Pyro4.expose
class MaestroSeguridad:
    def __init__(self):
        self.dataframe = self._cargar_y_preparar_datos()

    def _cargar_y_preparar_datos(self):
        """Carga solo lo esencial, optimizando memoria al máximo."""
        if not os.path.exists(RUTA_CSV):
            print("[INFO] Leyendo Excel (Modo Optimizado de Memoria)...")
            
            # 1. read_excel con 'usecols' evita cargar las 33 columnas en RAM
            df_inicial = pd.read_excel(
                RUTA_EXCEL, 
                sheet_name='1. Homicidios Intencionales',
                usecols=COLUMNAS_UTILES
            )
            
            print("[INFO] Procesando fechas y limpiando datos...")
            # 2. Extraer el Año
            df_inicial['fecha_infraccion'] = pd.to_datetime(df_inicial['fecha_infraccion'], errors='coerce')
            df_inicial['Anio'] = df_inicial['fecha_infraccion'].dt.year
            df_inicial = df_inicial.dropna(subset=['Anio'])
            df_inicial['Anio'] = df_inicial['Anio'].astype(int)
            
            # 3. Eliminar la columna de fecha completa (ya no la necesitamos y gasta memoria)
            df_inicial = df_inicial.drop(columns=['fecha_infraccion'])
            
            print("[INFO] Guardando CSV ligero...")
            df_inicial.to_csv(RUTA_CSV, sep=";", index=False)
            
        print("[INFO] Cargando dataset en memoria RAM con tipado estricto...")
        
        # 4. Usar tipos 'category' reduce el peso del DataFrame hasta en un 90%
        tipos_optimizados = {
            'tipo_muerte': 'category',
            'provincia': 'category',
            'arma': 'category',
            'Anio': 'int16' # Ocupa menos bits que int64
        }
        
        return pd.read_csv(RUTA_CSV, sep=";", dtype=tipos_optimizados)

    def filtrar_por_anios(self, anio_inicio, anio_fin):
        """Filtra y devuelve solo los registros del rango."""
        df_filtrado = self.dataframe[(self.dataframe['Anio'] >= anio_inicio) & 
                                     (self.dataframe['Anio'] <= anio_fin)]
        
        # Al tener solo 4 columnas, este diccionario viajará rapidísimo por la red
        return df_filtrado.to_dict(orient='records')

    def agregacion_inicial(self, anio_inicio, anio_fin):
        """Conteo de categorías de muerte."""
        # Calculamos la agregación usando el dataframe global
        df_filtrado = self.dataframe[(self.dataframe['Anio'] >= anio_inicio) & 
                                     (self.dataframe['Anio'] <= anio_fin)]
        
        if df_filtrado.empty: 
            return {}
            
        conteo = df_filtrado['tipo_muerte'].value_counts().to_dict()
        return conteo

def iniciar_servidor_pyro():
    daemon = Pyro4.Daemon()
    try:
        name_server = Pyro4.locateNS()
        uri_maestro = daemon.register(MaestroSeguridad)
        name_server.register("maestro.seguridad", uri_maestro)
        print("[LISTO] Nodo Maestro registrado. Memoria optimizada.")
        daemon.requestLoop()
    except Pyro4.errors.NamingError:
        print("[ERROR] No se pudo conectar al Name Server.")

if __name__ == "__main__":
    iniciar_servidor_pyro()