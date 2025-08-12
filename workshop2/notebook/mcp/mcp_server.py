from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic_ai import Agent
from datetime import datetime, timedelta
import json
import random
import logging
import os
import logfire
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.getLogger("openai").setLevel(logging.CRITICAL)
logging.getLogger("mcp.server").setLevel(logging.CRITICAL)
logging.getLogger("fastmcp").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("httpcore").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("openai._client").setLevel(logging.CRITICAL) 

load_dotenv()

# Configurar Logfire
logfire.configure(
    service_name="mcp-creative-server",
    service_version="1.0.0",
    environment="development",
    token=os.getenv("LOGFIRE_TOKEN"),
    console=False
)

logfire.instrument_pydantic()
logfire.instrument_requests()

server = FastMCP('Creative AI Tools Server')

# Agentes especializados
story_agent = Agent('openai:gpt-4o-mini', 
    system_prompt='''Eres un narrador interactivo experto. Creas historias envolventes donde el usuario puede tomar decisiones que afectan el rumbo de la narrativa. Siempre presenta 2-3 opciones claras al final de cada segmento.''')

debate_agent = Agent('openai:gpt-4o-mini',
    system_prompt='''Eres un debatidor experto que puede representar cualquier perspectiva de forma convincente y respetuosa. Presenta argumentos sólidos, usa evidencia y mantén un tono académico pero accesible.''')

learning_agent = Agent('openai:gpt-4o-mini',
    system_prompt='''Eres un tutor personalizado que adapta explicaciones según el nivel del estudiante. Usas analogías, ejemplos prácticos y verificas la comprensión antes de avanzar.''')

# Estados de sesión (en producción usarías una base de datos)
story_sessions = {}
learning_sessions = {}

# HERRAMIENTA 1: NARRATIVA INTERACTIVA
@server.tool()
async def interactive_story(user_id: str, action: str = "start", choice: Optional[str] = None, genre: str = "aventura") -> Dict:
    """
    Crea y continúa historias interactivas donde las decisiones del usuario afectan el desarrollo.
    
    Args:
        user_id: Identificador único del usuario
        action: 'start' para nueva historia, 'continue' para continuar
        choice: La decisión tomada por el usuario (para continuar)
        genre: Género de la historia (aventura, misterio, sci-fi, fantasy, horror)
    """
    
    if action == "start":
        prompt = f"Inicia una historia interactiva de {genre}. Crea un escenario intrigante, presenta al protagonista y termina con 2-3 opciones claras para que el usuario elija. Máximo 200 palabras."
        
        response = await story_agent.run(prompt)
        
        story_sessions[user_id] = {
            "story": response.output,
            "chapter": 1,
            "genre": genre,
            "history": [response.output]
        }
        
        return {
            "chapter": 1,
            "story": response.output,
            "status": "awaiting_choice"
        }
    
    elif action == "continue" and choice:
        if user_id not in story_sessions:
            return {"error": "No hay historia activa. Usa action='start' primero."}
        
        session = story_sessions[user_id]
        
        prompt = f"""
        Historia anterior: {session['history'][-1]}
        
        El usuario eligió: {choice}
        
        Continúa la historia de {session['genre']} incorporando esta decisión. 
        Desarrolla las consecuencias de la elección, añade nuevos elementos narrativos 
        y termina con 2-3 nuevas opciones. Máximo 200 palabras.
        """
        
        response = await story_agent.run(prompt)
        
        session['chapter'] += 1
        session['history'].append(response.output)
        
        return {
            "chapter": session['chapter'],
            "story": response.output,
            "status": "awaiting_choice"
        }
    
    else:
        return {"error": "Acción no válida. Usa 'start' o 'continue' con choice."}


# HERRAMIENTA 2: ARENA DE DEBATES
@server.tool()
async def debate_arena(topic: str, position_a: str, position_b: str, rounds: int = 3) -> Dict:
    """
    Simula un debate estructurado entre dos perspectivas sobre un tema.
    
    Args:
        topic: El tema a debatir
        position_a: Primera posición o perspectiva
        position_b: Segunda posición o perspectiva 
        rounds: Número de rondas de debate (1-5)
    """
    
    if rounds < 1 or rounds > 5:
        return {"error": "El número de rondas debe estar entre 1 y 5"}
    
    debate_results = {
        "topic": topic,
        "positions": {"A": position_a, "B": position_b},
        "rounds": []
    }
    
    context_a = f"Tema: {topic}\nTu posición: {position_a}"
    context_b = f"Tema: {topic}\nTu posición: {position_b}"
    
    for round_num in range(1, rounds + 1):
        # Argumento de la posición A
        prompt_a = f"""
        {context_a}
        
        Ronda {round_num}/{rounds}. Presenta un argumento sólido y convincente 
        para defender tu posición. Usa evidencia, lógica y ejemplos concretos.
        Máximo 150 palabras.
        """
        
        if round_num > 1:
            prompt_a += f"\n\nContexto previo: {debate_results['rounds'][-1]['argument_b']}"
        
        arg_a = await debate_agent.run(prompt_a)
        
        # Argumento de la posición B
        prompt_b = f"""
        {context_b}
        
        Ronda {round_num}/{rounds}. Responde al argumento anterior y presenta 
        tu contraargumento. Usa evidencia, lógica y ejemplos concretos.
        Máximo 150 palabras.
        
        Argumento a refutar: {arg_a.output}
        """
        
        arg_b = await debate_agent.run(prompt_b)
        
        debate_results["rounds"].append({
            "round": round_num,
            "argument_a": arg_a.output,
            "argument_b": arg_b.output
        })
    
    # Síntesis final
    synthesis_prompt = f"""
    Analiza este debate completo y proporciona:
    1. Un resumen de los puntos clave de cada posición
    2. Las fortalezas de cada argumento
    3. Posibles puntos de consenso o síntesis
    
    Debate completo: {json.dumps(debate_results, indent=2)}
    """
    
    synthesis = await debate_agent.run(synthesis_prompt)
    debate_results["synthesis"] = synthesis.output
    
    return debate_results


# HERRAMIENTA 3: TUTOR ADAPTATIVO
@server.tool()
async def adaptive_tutor(user_id: str, subject: str, question: Optional[str] = None, difficulty: str = "intermedio") -> Dict:
    """
    Tutor personalizado que adapta explicaciones según el progreso del estudiante.
    
    Args:
        user_id: Identificador del estudiante
        subject: Materia o tema a aprender
        question: Pregunta específica (opcional)
        difficulty: Nivel de dificultad (principiante, intermedio, avanzado)
    """
    
    if user_id not in learning_sessions:
        learning_sessions[user_id] = {
            "subjects": {},
            "learning_style": "visual",  # Se adaptaría según interacciones
            "progress": {}
        }
    
    session = learning_sessions[user_id]
    
    if subject not in session["subjects"]:
        session["subjects"][subject] = {
            "level": difficulty,
            "topics_covered": [],
            "questions_asked": 0,
            "correct_answers": 0
        }
    
    subject_data = session["subjects"][subject]
    
    if question:
        # Responder pregunta específica
        prompt = f"""
        Estudiante nivel {subject_data['level']} pregunta sobre {subject}: "{question}"
        
        Proporciona una explicación clara y adaptada a su nivel. Incluye:
        1. Respuesta directa
        2. Analogía o ejemplo práctico
        3. Una pregunta de verificación de comprensión
        4. Sugerencia para el siguiente paso de aprendizaje
        
        Historial del estudiante: {subject_data['topics_covered'][-3:]}
        """
        
        response = await learning_agent.run(prompt)
        subject_data['questions_asked'] += 1
        
        return {
            "response": response.output,
            "progress": {
                "questions_asked": subject_data['questions_asked'],
                "success_rate": f"{(subject_data['correct_answers']/max(1,subject_data['questions_asked']))*100:.1f}%"
            }
        }
    
    else:
        # Generar lección introductoria
        prompt = f"""
        Crea una lección introductoria de {subject} para nivel {difficulty}.
        
        Estructura:
        1. Pregunta o situación intrigante para despertar curiosidad
        2. Explicación clara con analogías
        3. Ejemplo práctico
        4. 2-3 preguntas para verificar comprensión
        5. Vista previa del siguiente tema
        
        Máximo 300 palabras, estilo conversacional.
        """
        
        response = await learning_agent.run(prompt)
        subject_data['topics_covered'].append(f"Introducción a {subject}")
        
        return {
            "lesson": response.output,
            "subject": subject,
            "level": difficulty,
            "progress": {
                "topics_covered": len(subject_data['topics_covered']),
                "questions_asked": subject_data['questions_asked']
            }
        }


# Herramienta bonus: Reset de sesiones
@server.tool()
async def reset_session(user_id: str, session_type: str = "all") -> Dict:
    """Reinicia las sesiones del usuario"""
    
    if session_type == "story" or session_type == "all":
        if user_id in story_sessions:
            del story_sessions[user_id]
    
    if session_type == "learning" or session_type == "all":
        if user_id in learning_sessions:
            del learning_sessions[user_id]
    
    return {"message": f"Sesión {session_type} reiniciada para usuario {user_id}"}


if __name__ == '__main__':
    server.run()