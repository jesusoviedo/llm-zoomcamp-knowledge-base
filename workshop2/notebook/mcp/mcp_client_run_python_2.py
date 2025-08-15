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

agent_data_analysis = Agent(
    'openai:gpt-4o-mini',
    toolsets=[server],
    system_prompt=(
        'Eres un analista de datos experto. Usa Python para realizar '
        'análisis estadísticos detallados y crear visualizaciones cuando sea apropiado.'
    )
)

async def analyze_sales_data():
    async with agent_data_analysis:
        result = await agent_data_analysis.run('''
        Analiza estos datos de ventas y proporciona insights:
        - Ventas mensuales: [15000, 18000, 22000, 19000, 25000, 28000, 30000, 26000, 23000, 27000, 31000, 35000]
        - Costos mensuales: [8000, 9500, 11000, 10000, 13000, 14500, 15000, 13500, 12000, 14000, 16000, 18000]
        
        Calcula:
        1. Margen de beneficio por mes
        2. Tendencia de crecimiento
        3. Proyección para los próximos 3 meses
        4. Recomendaciones basadas en los datos
        ''')
        print(result.output)

if __name__ == '__main__':
    asyncio.run(analyze_sales_data())