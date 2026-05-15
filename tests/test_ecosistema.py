import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nodo_logico_grpc')))

import archivo_pb2
import archivo_pb2_grpc

def test_conexion_grpc_caida():
    """Prueba que el sistema maneje bien el error si el Nodo gRPC no está."""
    print("Iniciando prueba de tolerancia a fallos...")
    canal = grpc.insecure_channel('localhost:50051')
    cliente = archivo_pb2_grpc.MotorAnaliticaStub(canal)
    
    filtro = archivo_pb2.FiltroAnios(anio_inicio=2020, anio_fin=2020)
    
    try:
        respuesta = cliente.ObtenerAgregacionInicial(filtro)
        print("Éxito: Servicios conectados correctamente.")
    except grpc.RpcError as e:
        print("Tolerancia a fallos correcta. Excepción capturada.")
        print(f"Estado: {e.code()} | Detalle: {e.details()}")

if __name__ == "__main__":
    test_conexion_grpc_caida()