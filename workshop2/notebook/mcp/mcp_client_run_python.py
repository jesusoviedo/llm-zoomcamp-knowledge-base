import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

# Configuración del servidor MCP Run Python
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

# Agente con capacidad de ejecutar Python
agent = Agent(
    'openai:gpt-4o-mini',
    toolsets=[server],
    system_prompt=(
        'Eres un asistente de programación que puede ejecutar código Python '
        'para resolver problemas matemáticos y de análisis de datos.'
    )
)

async def main():
    async with agent:
        result = await agent.run(
            'Calcula la media y desviación estándar de los números [1, 2, 3, 4, 5, 10, 100]'
        )
        print(result.output)

if __name__ == '__main__':
    asyncio.run(main())