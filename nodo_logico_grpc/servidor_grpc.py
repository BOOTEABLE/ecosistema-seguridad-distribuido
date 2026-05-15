import grpc
from concurrent import futures
import pandas as pd
import json
import Pyro4

import archivo_pb2
import archivo_pb2_grpc

class MotorAnaliticaServicer(archivo_pb2_grpc.MotorAnaliticaServicer):
    def __init__(self):
        self.cliente_pyro = Pyro4.Proxy("PYRONAME:maestro.seguridad")

    def _verificar_conexion_pyro(self, context):
        try:
            self.cliente_pyro._pyroBind()
        except Exception as error:
            context.abort(grpc.StatusCode.UNAVAILABLE, "Nodo Maestro Pyro4 no responde")

    def _procesar_frecuencia(self, request, context, columna_objetivo):
        self._verificar_conexion_pyro(context)
        try:
            datos_brutos = self.cliente_pyro.filtrar_por_anios(request.anio_inicio, request.anio_fin)
            df = pd.DataFrame(datos_brutos)
            
            if df.empty:
                return archivo_pb2.RespuestaFrecuencias(datos=[])

            conteo = df[columna_objetivo].value_counts()
            lista_items = [archivo_pb2.ItemFrecuencia(categoria=str(k), cantidad=int(v)) 
                           for k, v in conteo.items()]
            
            return archivo_pb2.RespuestaFrecuencias(datos=lista_items)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    def ObtenerFrecuenciaProvincia(self, request, context):
        # CORRECCIÓN: 'provincia' en minúsculas estrictas
        return self._procesar_frecuencia(request, context, 'provincia') 

    def ObtenerFrecuenciaArma(self, request, context):
        # CORRECCIÓN: 'arma' en minúsculas estrictas
        return self._procesar_frecuencia(request, context, 'arma') 

    def ObtenerAgregacionInicial(self, request, context):
        self._verificar_conexion_pyro(context)
        try:
            conteo = self.cliente_pyro.agregacion_inicial(request.anio_inicio, request.anio_fin)
            lista_items = [archivo_pb2.ItemFrecuencia(categoria=str(k), cantidad=int(v)) 
                           for k, v in conteo.items()]
            return archivo_pb2.RespuestaFrecuencias(datos=lista_items)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    def ObtenerResumenTabla(self, request, context):
        self._verificar_conexion_pyro(context)
        try:
            datos_brutos = self.cliente_pyro.filtrar_por_anios(request.anio_inicio, request.anio_fin)
            df = pd.DataFrame(datos_brutos)
            
            # CORRECCIÓN: Eliminamos el .head(100) para enviar todos los registros
            json_df = df.to_json(orient='records') 
            return archivo_pb2.RespuestaTabla(json_dataframe=json_df, total_registros=len(df))
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

def iniciar_servidor_grpc():
    # CORRECCIÓN: Ampliamos el límite de gRPC a 50MB para soportar todo el dataset
    opciones_red = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024)
    ]
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=opciones_red)
    archivo_pb2_grpc.add_MotorAnaliticaServicer_to_server(MotorAnaliticaServicer(), servidor)
    servidor.add_insecure_port('[::]:50051')
    print("[LISTO] Nodo Lógico gRPC ejecutándose en el puerto 50051 (Canal Ampliado)...")
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor_grpc()