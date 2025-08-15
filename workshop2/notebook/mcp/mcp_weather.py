from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os
import asyncio

print("Inicializando MCP Weather...")

# Cargar variables de entorno
load_dotenv()

# Obtener API KEY
api_key = os.getenv("OPENWEATHER_API_KEY")

# Inicializar servidor FastMCP
mcp = FastMCP("weather", dependencies=["requests"])
print("Servidor MCP creado con dependencias: requests")

@mcp.tool()
def get_weather(city: str) -> dict[str, Any]:
    """Get current weather for a location"""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY no encontrada en las variables de entorno")
        
        # Obtener coordenadas de la ciudad
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            raise ValueError(f"No se encontró la ciudad: {city}")
        
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        
        # Obtener datos meteorológicos
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["main"]
        
        return {
            "location": city,
            "temperature": temperature,
            "description": description,
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
        return {"error": f"Error de red: {str(e)}"}
    except (KeyError, IndexError) as e:
        print(f"Error procesando datos de la API: {e}")
        return {"error": f"Error procesando datos de la API: {str(e)}"}
    except ValueError as e:
        print(f"Error de validación: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error inesperado: {e}")
        return {"error": f"Error inesperado: {str(e)}"}

def main():
    """Función principal para ejecutar el servidor MCP"""
    print("\n" + "="*60)
    print("SERVIDOR MCP WEATHER")
    print("="*60)
    print("Herramientas disponibles:")
    print("   • get_weather(city) - Obtiene clima actual")
    print("="*60)
    
    try:
        print("Iniciando servidor MCP...")
        print("Presiona Ctrl+C para detener")
        print("Esperando conexiones MCP...")
        print("="*60 + "\n")
        
        mcp.run()
        
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"\nError al ejecutar el servidor: {e}")

if __name__ == "__main__":
    main()