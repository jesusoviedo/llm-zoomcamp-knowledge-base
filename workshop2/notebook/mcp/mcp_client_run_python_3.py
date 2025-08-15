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

agent_validation = Agent(
    'openai:gpt-4o-mini',
    toolsets=[server],
    system_prompt=(
        'Eres un experto en validación de datos. Usa Pydantic para crear '
        'modelos robustos y validar datos de entrada según las especificaciones.'
    )
)

async def validate_api_data():
    async with agent_validation:
        result = await agent_validation.run('''
        Crea un modelo Pydantic para validar datos de un API de e-commerce:
        
        Requisitos:
        - ID del producto (string, formato UUID)
        - Nombre (string, 3-100 caracteres)
        - Precio (decimal, mayor a 0, máximo 2 decimales)
        - Categoría (enum: electronics, clothing, books, home, sports)
        - Stock (entero, >= 0)
        - Fecha de creación (datetime)
        - Email del vendedor (email válido)
        - Descripción (opcional, máximo 500 caracteres)
        
        Luego valida estos datos de prueba:
        {
            "product_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Smartphone XYZ",
            "price": "299.99",
            "category": "electronics",
            "stock": 50,
            "created_at": "2024-01-15T10:30:00Z",
            "seller_email": "vendor@example.com",
            "description": "High-performance smartphone with great camera"
        }
        ''')

        print(result.output)

if __name__ == '__main__':
    asyncio.run(validate_api_data())