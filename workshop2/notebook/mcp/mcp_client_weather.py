import asyncio
import json
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ExternalMCPClient:
    def __init__(self, server_command=None):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.server_process = None
        self.message_id = 1
        self.server_command = server_command or [sys.executable, "mcp_weather.py"]
        
        # Ciudades del Paraguay
        self.paraguay_cities = [
            "Asunción", 
            "Ciudad del Este", 
            "San Lorenzo",
            "Luque",
            "Capiatá",
            "Lambaré",
            "Fernando de la Mora"
        ]

    async def connect_to_external_server(self):
        """
        Se conecta a un servidor MCP externo que YA ESTÁ EJECUTÁNDOSE.
        Inicia el servidor como subproceso para comunicación STDIO.
        """
        try:
            print("Conectando a servidor MCP externo...")
            
            # CONECTAR al servidor existente via STDIO
            self.server_process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            print("Conectado al servidor MCP")
            return True
            
        except Exception as e:
            print(f"Error conectando al servidor: {e}")
            return False

    async def send_request(self, method: str, params: dict = None) -> dict:
        """Enviar solicitud JSON-RPC al servidor"""
        try:

            message = {
                "jsonrpc": "2.0",
                "id": self.message_id,
                "method": method
            }
        
            if params:
                message["params"] = params
                
            self.message_id += 1

            # Enviar
            message_str = json.dumps(message) + "\n"
            # Descomentar para mostrar mensaje enviado
            # print(f"Enviando solicitud: {json.dumps(message, indent=2)}")
            self.server_process.stdin.write(message_str.encode())
            await self.server_process.stdin.drain()

            # Recibir
            response_line = await self.server_process.stdout.readline()
            if not response_line:
                raise Exception("Sin respuesta del servidor")
                
            return json.loads(response_line.decode().strip())
            
        except Exception as e:
            print(f"Error en comunicación: {e}")
            return {"error": str(e)}

    async def send_notification(self, method: str, params: dict = None):
        """Enviar una notificación JSON-RPC (sin id, no espera respuesta)"""
        try:
            message = {
                "jsonrpc": "2.0",
                "method": method
            }
            if params is not None:
                message["params"] = params

            message_str = json.dumps(message) + "\n"
            # Descomentar para mostrar notificacion enviado
            # print(f"Enviando notificacion: {json.dumps(message, indent=2)}")
            self.server_process.stdin.write(message_str.encode())
            await self.server_process.stdin.drain()
        except Exception as e:
            print(f"Error enviando notificación: {e}")

    async def initialize(self):
        """Handshake inicial con servidor"""
        try:
            print("Inicializando protocolo MCP...")
            
            init_params = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {
                    "name": "weather-client",
                    "version": "1.0.0"
                }
            }

            response = await self.send_request("initialize", init_params)
            # Descomentar para mostrar respuesta
            # print("Respuesta inicial:", json.dumps(response, indent=2))
            
            if "error" in response:
                print(f"Error en inicialización: {response['error']}")
                return False
                
            # Notificación de inicialización
            await self.send_notification("notifications/initialized")
            
            print("Protocolo MCP inicializado")
            return True
            
        except Exception as e:
            print(f"Error en inicialización: {e}")
            return False

    async def list_tools(self):
        """Listar herramientas del servidor"""
        try:
            print("Obteniendo herramientas disponibles...")
            
            response = await self.send_request("tools/list")
            # Descomentar para mostrar respuesta
            # print("Respuesta de herramientas:", json.dumps(response, indent=2))
            
            if "error" in response:
                print(f"Error: {response['error']}")
                return []
                
            if "result" in response and "tools" in response["result"]:
                tools = response["result"]["tools"]
                print(f"Herramientas encontradas: {len(tools)}")
                
                for tool in tools:
                    print(f"  - {tool['name']}: {tool.get('description', 'Sin descripción')}")
                
                return [tool["name"] for tool in tools]
            
            return []
                
        except Exception as e:
            print(f"Error listando herramientas: {e}")
            return []

    async def call_tool(self, name: str, arguments: dict):
        """Ejecutar herramienta en servidor externo"""
        try:
            # Descomentar para mostrar llamada a herramienta
            #print(f"Ejecutando: {name} con args: {arguments}")
            
            params = {
                "name": name,
                "arguments": arguments
            }
            
            response = await self.send_request("tools/call", params)
            
            if "error" in response:
                print(f"Error en herramienta: {response['error']}")
                return {"error": response["error"]}
                
            if "result" in response:
                result = response["result"]
                
                # Extraer contenido
                if "content" in result and result["content"]:
                    content = result["content"][0]
                    if content["type"] == "text":
                        try:
                            return json.loads(content["text"])
                        except json.JSONDecodeError:
                            return {"result": content["text"]}
                
                return result
            
            return {"error": "Respuesta inesperada"}
                
        except Exception as e:
            print(f"Error ejecutando herramienta: {e}")
            return {"error": str(e)}

    async def get_paraguay_weather(self):
        """Obtener clima de Paraguay usando servidor"""
        print(f"\n{'='*50}")
        print("CONSULTANDO CLIMA VIA SERVIDOR MCP")
        print(f"{'='*50}")
        
        weather_data = []
        
        for city in self.paraguay_cities:
            print(f"\nConsultando: {city}")
            
            result = await self.call_tool("get_weather", {"city": city})
            
            if "error" not in result:
                weather_data.append(result)
                temp = result.get("temperature", "N/A")
                desc = result.get("description", "N/A")
                print(f"{city}: {temp}°C - {desc}")
            else:
                print(f"{city}: {result['error']}")
                weather_data.append({
                    "location": city,
                    "error": result["error"]
                })
                
        return weather_data

    async def analyze_with_openai(self, weather_data):
        """Análisis con OpenAI"""
        try:            
            prompt = "Analiza estos datos meteorológicos de Paraguay:\n\n"
            
            for data in weather_data:
                if "error" not in data:
                    prompt += f"- {data.get('location', 'N/A')}: {data.get('temperature', 'N/A')}°C, "
                    prompt += f"{data.get('description', 'N/A')}\n"
                else:
                    prompt += f"- {data.get('location', 'N/A')}: Error en consulta\n"
            
            prompt += "\nProporciona:\n1. Resumen del clima\n2. Ciudad más calurosa/fresca\n"
            prompt += "3. Recomendaciones\n4. Patrones observados"
            
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un meteorólogo experto en Paraguay. Analiza datos de forma clara y útil."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error con OpenAI: {str(e)}"

    async def disconnect(self):
        """Desconectar del servidor"""
        try:
            if self.server_process:
                print("\nDesconectando del servidor MCP...")
                self.server_process.terminate()
                await self.server_process.wait()
                print("Desconectado")
        except Exception as e:
            print(f"Error desconectando: {e}")

async def main():
    """
    Función principal para cliente de servidor externo
    """
    client = None
    
    try:
        print("=" * 40)
        print("CLIENTE MCP WEATHER")
        print("=" * 40)
        
        # Verificar variables de entorno
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY no encontrada")
            return
        
        # Crear cliente
        client = ExternalMCPClient()
        
        # Conectar a servidor externo
        if not await client.connect_to_external_server():
            print("No se pudo conectar al servidor MCP")
            print("Asegúrate de que esté ejecutándose en otro terminal")
            return
        
        # Inicializar protocolo
        if not await client.initialize():
            return
        
        # Listar herramientas
        tools = await client.list_tools()
        if not tools:
            print("No hay herramientas disponibles")
            return
        
        # Obtener clima
        weather_data = await client.get_paraguay_weather()
        
        # Analizar con OpenAI
        analysis = await client.analyze_with_openai(weather_data)
        
        # Mostrar resultados
        print(f"\n{'='*50}")
        print("ANÁLISIS METEOROLÓGICO")
        print(f"{'='*50}")
        print(analysis)
        print(f"{'='*50}")
        
        print("\nCliente completado exitosamente!")
        
    except KeyboardInterrupt:
        print("\nProceso interrumpido")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client:
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())