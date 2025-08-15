import asyncio
import uvicorn
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

app = FastAPI(title="Code Execution API")

class CodeRequest(BaseModel):
    code: str
    timeout: int = 30

class CodeResponse(BaseModel):
    status: str
    output: str

@app.post("/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    """
    API endpoint que permite a usuarios ejecutar código Python de forma segura
    """
    try:
        # Configurar el agente con timeout personalizado
        execution_agent = Agent(
            'openai:gpt-4o-mini',
            toolsets=[server],
            system_prompt=f'''
            Ejecuta el siguiente código Python en el sandbox:
            
            {request.code}
            
            Importante:
            - Si el código tiene errores, repórtalos claramente
            - Si el código es potencialmente peligroso, no lo ejecutes
            - Limita la ejecución a {request.timeout} segundos conceptualmente
            '''
        )
        
        async with execution_agent:
            result = await execution_agent.run("Ejecuta el código proporcionado")
            
            return CodeResponse(
                status="success",
                output=result.output
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ejecutando código: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("mcp_client_run_python_5:app", host="0.0.0.0", port=8000, reload=True)