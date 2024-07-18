from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random
import time
import requests
import numpy as np

def push_metrics(registry, retries=3, delay=5):
    for i in range(retries):
        try:
            push_to_gateway('pushgateway:9091', job='benchmark-cpu', registry=registry)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar métricas: {e}. Tentativa {i+1} de {retries}")
            time.sleep(delay)
    return False

def benchmark_matriz(dimensao):
    registry = CollectorRegistry()
    cpu_usage = Gauge('cpu_usage', 'CPU usage percentage', registry=registry)
    memory_usage = Gauge('memory_usage', 'Memory usage percentage', registry=registry)
    request_time = Gauge('request_processing_seconds', 'Time spent processing request', registry=registry)
    flops_gauge = Gauge('flops', 'Floating Point Operations Per Second', registry=registry)

    cpu_usage.set(random.uniform(0, 100))
    memory_usage.set(random.uniform(0, 100))

    matriz_a = np.random.rand(dimensao, dimensao)
    matriz_b = np.random.rand(dimensao, dimensao)
    
    start_time = time.time()
    resultado = np.dot(matriz_a, matriz_b)
    duration = time.time() - start_time
    request_time.set(duration)

    num_operacoes = 2 * dimensao**3  
    flops = num_operacoes / duration
    flops_gauge.set(flops)

    if not push_metrics(registry):
        print("Falha ao enviar métricas após múltiplas tentativas.")

if __name__ == '__main__':
    while True:
        benchmark_matriz(100)
        time.sleep(10)
