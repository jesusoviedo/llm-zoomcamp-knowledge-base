import math
from datetime import datetime
from mcp.server.fastmcp import FastMCP

app = FastMCP()

@app.tool()
def calcular_interes_compuesto(principal: float, tasa: float, periodos: int) -> float:
    """
    Calcula el valor final con interés compuesto.

    - principal: Monto inicial
    - tasa: Tasa de interés anual en porcentaje (ej. 5.0)
    - periodos: Número de años
    """
    return principal * (1 + tasa / 100) ** periodos


@app.tool()
def polar_a_cartesiana(radio: float, angulo_grados: float) -> tuple:
    """
    Convierte coordenadas polares a cartesianas (x, y).
    """
    angulo_radianes = math.radians(angulo_grados)
    x = radio * math.cos(angulo_radianes)
    y = radio * math.sin(angulo_radianes)
    return (x, y)


@app.tool()
def factorial(n: int) -> int:
    """
    Calcula el factorial de un número entero positivo.
    """
    if n < 0:
        raise ValueError("El número debe ser positivo.")
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


@app.tool()
def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en kilómetros entre dos coordenadas geográficas usando la fórmula de Haversine.
    """
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@app.tool()
def calculate_days_between_dates(start_date: datetime, end_date: datetime) -> int:
    """
    Calcula la diferencia en días entre dos fechas.
    
    Args:
        start_date (datetime): Fecha de inicio.
        end_date (datetime): Fecha de fin.
        
    Returns:
        int: Número de días entre las dos fechas.
    """
    return (end_date - start_date).days

if __name__ == '__main__':
    app.run(transport='streamable-http')