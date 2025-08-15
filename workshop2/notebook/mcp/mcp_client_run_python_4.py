import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

server = MCPServerStdio(
    'deno',
    args=[
        'run',
        '-N',
        '-R=node_modules',
        '-W=node_modules',
        '--node-modules-dir=auto',
        'jsr:@pydantic/mcp-run-python',
        'stdio',
    ]
)

agent_visualization = Agent(
    'openai:gpt-4o-mini',
    toolsets=[server],
    system_prompt=(
        'Eres un especialista en visualización de datos. Crea gráficos '
        'informativos y estéticamente agradables usando matplotlib.'
    )
)

async def create_visualizations():
    async with agent_visualization:
        result = await agent_visualization.run('''
        Crea una visualización completa para estos datos de temperatura:
        
        Ciudades: ["Asunción", "Ciudad del Este", "Encarnación", "Concepción", "Pedro Juan Caballero"]
        Temperaturas promedio (°C): [28, 26, 27, 29, 25]
        Humedad (%): [78, 82, 75, 70, 85]
        
        Crea:
        1. Un gráfico de barras para las temperaturas
        2. Un gráfico de dispersión temperatura vs humedad
        3. Un gráfico combinado con ambas métricas
        
        Asegúrate de incluir títulos, etiquetas de ejes, leyendas y colores apropiados.
        ''')
        print(result.output)

if __name__ == '__main__':
    asyncio.run(create_visualizations())