import asyncio
from dotenv import load_dotenv
import os
import logging
import json
import logfire
import subprocess
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

# === CONFIGURACIÓN DE LOGFIRE ===
# Configurar Logfire condicionalmente
if os.getenv("LOGFIRE_TOKEN"):
    logfire.configure(
        service_name="mcp-tutor-client",
        service_version="1.0.0",
        environment="development",
        token=os.getenv("LOGFIRE_TOKEN"),
        console=False
    )
    LOGFIRE_ENABLED = True
else:
    LOGFIRE_ENABLED = False


# === FUNCIONES HELPER PARA TRACKING CONDICIONAL ===
def safe_span(name, **kwargs):
    """Crea un span solo si Logfire está habilitado"""
    if LOGFIRE_ENABLED:
        return logfire.span(name, **kwargs)
    else:
        from contextlib import nullcontext
        return nullcontext()

def safe_info(message, **kwargs):
    """Log info solo si Logfire está habilitado"""
    if LOGFIRE_ENABLED:
        logfire.info(message, **kwargs)

def safe_warning(message, **kwargs):
    """Log warning solo si Logfire está habilitado"""
    if LOGFIRE_ENABLED:
        logfire.warning(message, **kwargs)

def safe_error(message, **kwargs):
    """Log error solo si Logfire está habilitado"""
    if LOGFIRE_ENABLED:
        logfire.error(message, **kwargs)

def display_progress(progress_data):
    """Muestra el progreso del estudiante de forma clara"""
    safe_info("Displaying student progress", progress_data=progress_data)
    
    print("\n" + "="*50)
    print("PROGRESO DEL ESTUDIANTE:")
    print("="*50)
    
    if 'topics_covered' in progress_data:
        print(f"Temas cubiertos: {progress_data['topics_covered']}")
    
    if 'questions_asked' in progress_data:
        print(f"Preguntas realizadas: {progress_data['questions_asked']}")
    
    if 'success_rate' in progress_data:
        print(f"Tasa de éxito: {progress_data['success_rate']}")
    
    print("="*50)

def get_user_input(prompt, allow_empty=False):
    """Obtiene entrada del usuario con validación"""
    safe_info("Requesting user input", prompt=prompt, allow_empty=allow_empty)
    
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input or allow_empty:
                safe_info("User input received", 
                         input_length=len(user_input), 
                         is_empty=not bool(user_input))
                return user_input
            else:
                print("No puedes dejar este campo vacío.")
                safe_warning("Empty input rejected")
        except KeyboardInterrupt:
            print("\nSesión interrumpida!")
            safe_warning("Session interrupted by user")
            return None
        except Exception as e:
            print(f"Error: {e}")
            safe_error("Error getting user input", error=str(e))

def select_difficulty():
    """Permite al usuario seleccionar el nivel de dificultad"""
    with safe_span("select_difficulty"):
        difficulties = ["principiante", "intermedio", "avanzado"]
        
        print("\nNiveles de dificultad disponibles:")
        for i, difficulty in enumerate(difficulties, 1):
            print(f"{i}. {difficulty.title()}")
        
        while True:
            choice = get_user_input(f"\nElige un nivel (1-{len(difficulties)}): ")
            if choice and choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(difficulties):
                    selected_difficulty = difficulties[choice_num - 1]
                    safe_info("Difficulty selected", 
                             difficulty=selected_difficulty, 
                             choice_number=choice_num)
                    return selected_difficulty
            print("Opción inválida")
            safe_warning("Invalid difficulty choice", choice=choice)

def select_subject():
    """Permite al usuario seleccionar o escribir una materia"""
    with safe_span("select_subject"):
        suggested_subjects = [
            "Matemáticas", "Física", "Química", "Programación", 
            "Historia", "Biología", "Literatura", "Machine Learning",
            "Inglés", "Filosofía"
        ]
        
        safe_info("Showing subject options", total_subjects=len(suggested_subjects))
        
        print("\nMaterias sugeridas:")
        for i, subject in enumerate(suggested_subjects, 1):
            print(f"{i}. {subject}")
        print(f"{len(suggested_subjects) + 1}. Escribir otra materia")
        
        while True:
            choice = get_user_input(f"\nElige una materia (1-{len(suggested_subjects) + 1}): ")
            if choice and choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(suggested_subjects):
                    selected_subject = suggested_subjects[choice_num - 1]
                    safe_info("Predefined subject selected", 
                             subject=selected_subject,
                             choice_number=choice_num)
                    return selected_subject
                elif choice_num == len(suggested_subjects) + 1:
                    custom_subject = get_user_input("Escribe la materia: ")
                    if custom_subject:
                        safe_info("Custom subject selected", subject=custom_subject)
                        return custom_subject
            print("Opción inválida")
            safe_warning("Invalid subject choice", choice=choice)

async def tutor_session():
    """Sesión completa de tutoría interactiva"""
    session_start_time = datetime.now()
    
    with safe_span("tutor_session") as span:
        safe_info("Starting interactive tutor session")
        
        print("BIENVENIDO AL TUTOR ADAPTATIVO")
        print("="*50)
        
        # Configuración inicial
        user_id = get_user_input("Ingresa tu nombre de estudiante (o presiona Enter para 'estudiante1'): ", allow_empty=True)
        if not user_id:
            user_id = "estudiante1"
        
        subject = select_subject()
        if not subject:
            safe_warning("No subject selected, ending session")
            return
            
        difficulty = select_difficulty()
        if not difficulty:
            safe_warning("No difficulty selected, ending session")
            return
        
        # Log configuración de sesión
        safe_info("Session configuration completed",
                 user_id=user_id,
                 subject=subject,
                 difficulty=difficulty)
        
        if LOGFIRE_ENABLED and span:
            span.set_attribute("user_id", user_id)
            span.set_attribute("subject", subject)
            span.set_attribute("difficulty", difficulty)
        
        server_params = StdioServerParameters(
            command='python', args=['mcp_server.py'], env=os.environ, stderr=subprocess.DEVNULL
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                with safe_span("mcp_session_initialization"):
                    await session.initialize()
                    safe_info("MCP session initialized")
                
                print(f"\nIniciando sesión de {subject} para {user_id} (Nivel: {difficulty})")
                print("="*60)
                
                # Obtener lección introductoria
                print("Generando lección introductoria...")
                
                with safe_span("introductory_lesson") as lesson_span:
                    result = await session.call_tool('adaptive_tutor', {
                        'user_id': user_id,
                        'subject': subject,
                        'difficulty': difficulty
                    })
                    
                    tutor_data = json.loads(result.content[0].text)
                    
                    lesson_length = len(tutor_data['lesson'])
                    safe_info("Introductory lesson generated",
                             lesson_length=lesson_length,
                             progress=tutor_data['progress'])
                    
                    if LOGFIRE_ENABLED and lesson_span:
                        lesson_span.set_attribute("lesson_length", lesson_length)
                
                print(f"\nLECCIÓN: {tutor_data['subject']} (Nivel: {tutor_data['level']})")
                print("-" * 60)
                print(tutor_data['lesson'])
                
                display_progress(tutor_data['progress'])
                
                # Sesión de preguntas y respuestas
                max_questions = 10
                question_count = 0
                questions_asked = []
                
                print(f"\nAhora puedes hacer preguntas sobre {subject}.")
                print("Escribe 'salir' para terminar la sesión.")
                print("Escribe 'progreso' para ver tu avance.")
                print("="*60)
                
                while question_count < max_questions:
                    with safe_span(f"question_{question_count + 1}") as q_span:
                        user_question = get_user_input(f"\nPregunta {question_count + 1}: ")
                        
                        if not user_question:
                            safe_info("Empty question, ending session")
                            break
                        
                        if user_question.lower() == 'salir':
                            print("Terminando sesión de tutoría...")
                            safe_info("User requested session end")
                            break
                        
                        if user_question.lower() == 'progreso':
                            with safe_span("progress_check"):
                                result = await session.call_tool('adaptive_tutor', {
                                    'user_id': user_id,
                                    'subject': subject,
                                    'difficulty': difficulty
                                })
                                tutor_data = json.loads(result.content[0].text)
                                display_progress(tutor_data['progress'])
                                safe_info("Progress check completed")
                            continue
                        
                        questions_asked.append(user_question)
                        
                        if LOGFIRE_ENABLED and q_span:
                            q_span.set_attribute("question", user_question)
                            q_span.set_attribute("question_length", len(user_question))
                        
                        print("Procesando tu pregunta...")
                        
                        try:
                            with safe_span("tutor_response") as r_span:
                                result = await session.call_tool('adaptive_tutor', {
                                    'user_id': user_id,
                                    'subject': subject,
                                    'question': user_question,
                                    'difficulty': difficulty
                                })
                                
                                tutor_data = json.loads(result.content[0].text)
                                
                                response_length = len(tutor_data['response'])
                                safe_info("Question processed successfully",
                                         question=user_question,
                                         response_length=response_length,
                                         progress=tutor_data['progress'])
                                
                                if LOGFIRE_ENABLED and r_span:
                                    r_span.set_attribute("response_length", response_length)
                            
                            print("\nRESPUESTA DEL TUTOR:")
                            print("-" * 40)
                            print(tutor_data['response'])
                            
                            display_progress(tutor_data['progress'])
                            
                            question_count += 1
                            
                        except Exception as e:
                            print(f"Error al procesar la pregunta: {e}")
                            safe_error("Error processing question",
                                     error=str(e),
                                     question=user_question)
                
                if question_count >= max_questions:
                    print(f"\nAlcanzaste el límite de {max_questions} preguntas por sesión.")
                    safe_info("Question limit reached", max_questions=max_questions)
                
                print(f"\nGracias por usar el tutor, {user_id}!")
                print("="*60)
                
                # Métricas finales de sesión
                session_duration = (datetime.now() - session_start_time).total_seconds()
                safe_info("Tutor session completed",
                         user_id=user_id,
                         subject=subject,
                         difficulty=difficulty,
                         questions_asked=question_count,
                         session_duration_seconds=session_duration,
                         total_questions_list=questions_asked)
                
                if LOGFIRE_ENABLED and span:
                    span.set_attribute("questions_asked", question_count)
                    span.set_attribute("session_duration", session_duration)

async def quick_tutor_demo():
    """Demostración rápida del tutor"""
    with safe_span("quick_tutor_demo"):
        safe_info("Starting quick tutor demo")
        
        print("DEMO RÁPIDA DEL TUTOR ADAPTATIVO")
        print("="*50)
        
        server_params = StdioServerParameters(
            command='python', args=['mcp_server.py'], env=os.environ, stderr=subprocess.DEVNULL
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                safe_info("Demo MCP session initialized")
                
                # Lección de Machine Learning
                print("1. Lección introductoria de Machine Learning...")
                with safe_span("demo_lesson"):
                    result = await session.call_tool('adaptive_tutor', {
                        'user_id': 'demo_student',
                        'subject': 'Machine Learning',
                        'difficulty': 'principiante'
                    })
                    
                    tutor_data = json.loads(result.content[0].text)
                    print(f"\nLección: {tutor_data['lesson']}")
                    display_progress(tutor_data['progress'])
                    safe_info("Demo lesson completed", lesson_length=len(tutor_data['lesson']))
                
                # Pregunta específica
                print("\n2. Pregunta específica sobre algoritmos...")
                with safe_span("demo_question_1"):
                    result = await session.call_tool('adaptive_tutor', {
                        'user_id': 'demo_student',
                        'subject': 'Machine Learning',
                        'question': '¿Cuál es la diferencia entre regresión y clasificación?',
                        'difficulty': 'intermedio'
                    })
                    
                    tutor_data = json.loads(result.content[0].text)
                    print(f"\nRespuesta: {tutor_data['response']}")
                    display_progress(tutor_data['progress'])
                    safe_info("Demo question 1 completed")
                
                # Otra pregunta más avanzada
                print("\n3. Pregunta avanzada sobre redes neuronales...")
                with safe_span("demo_question_2"):
                    result = await session.call_tool('adaptive_tutor', {
                        'user_id': 'demo_student',
                        'subject': 'Machine Learning',
                        'question': '¿Cómo funciona el backpropagation en redes neuronales?',
                        'difficulty': 'avanzado'
                    })
                    
                    tutor_data = json.loads(result.content[0].text)
                    print(f"\nRespuesta: {tutor_data['response']}")
                    display_progress(tutor_data['progress'])
                    safe_info("Demo question 2 completed")
        
        safe_info("Quick tutor demo completed")

async def subject_focused_session():
    """Sesión enfocada en una materia específica con ejemplos"""
    with safe_span("subject_focused_session"):
        subjects_examples = {
            "matemáticas": [
                "¿Qué es una derivada?",
                "¿Cómo resuelvo una ecuación cuadrática?",
                "Explícame los límites en cálculo"
            ],
            "programación": [
                "¿Qué es una función recursiva?",
                "¿Cuál es la diferencia entre lista y tupla en Python?",
                "¿Cómo funciona la programación orientada a objetos?"
            ],
            "física": [
                "¿Qué es la velocidad angular?",
                "Explícame las leyes de Newton",
                "¿Cómo funciona la relatividad especial?"
            ]
        }
        
        safe_info("Starting subject focused session", 
                 available_subjects=list(subjects_examples.keys()))
        
        print("SESIÓN ENFOCADA POR MATERIA")
        print("="*50)
        
        print("Materias con ejemplos predefinidos:")
        available_subjects = list(subjects_examples.keys())
        for i, subject in enumerate(available_subjects, 1):
            print(f"{i}. {subject.title()}")
        
        choice = get_user_input(f"\nElige una materia (1-{len(available_subjects)}): ")
        if not choice or not choice.isdigit():
            safe_warning("Invalid subject choice in focused session")
            return
        
        choice_num = int(choice)
        if not (1 <= choice_num <= len(available_subjects)):
            safe_warning("Subject choice out of range")
            return
        
        selected_subject = available_subjects[choice_num - 1]
        example_questions = subjects_examples[selected_subject]
        
        user_id = get_user_input("Tu nombre de estudiante: ", allow_empty=True) or "estudiante_enfocado"
        difficulty = select_difficulty()
        
        safe_info("Focused session configuration",
                 subject=selected_subject,
                 user_id=user_id,
                 difficulty=difficulty,
                 total_example_questions=len(example_questions))
        
        server_params = StdioServerParameters(
            command='python', args=['mcp_server.py'], env=os.environ, stderr=subprocess.DEVNULL
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print(f"\nSesión de {selected_subject.title()} para {user_id}")
                print("="*60)
                
                # Lección introductoria
                with safe_span("focused_intro_lesson"):
                    result = await session.call_tool('adaptive_tutor', {
                        'user_id': user_id,
                        'subject': selected_subject,
                        'difficulty': difficulty
                    })
                    
                    tutor_data = json.loads(result.content[0].text)
                    print("LECCIÓN INTRODUCTORIA:")
                    print(tutor_data['lesson'])
                    display_progress(tutor_data['progress'])
                
                # Preguntas predefinidas
                print(f"\nEjemplos de preguntas para {selected_subject}:")
                for i, question in enumerate(example_questions, 1):
                    with safe_span(f"example_question_{i}"):
                        print(f"\n{i}. Pregunta: {question}")
                        
                        result = await session.call_tool('adaptive_tutor', {
                            'user_id': user_id,
                            'subject': selected_subject,
                            'question': question,
                            'difficulty': difficulty
                        })
                        
                        tutor_data = json.loads(result.content[0].text)
                        print(f"   Respuesta: {tutor_data['response'][:200]}...")
                        
                        safe_info("Example question processed",
                                 question_number=i,
                                 question=question,
                                 response_length=len(tutor_data['response']))
                        
                        if i < len(example_questions):
                            input("\nPresiona Enter para continuar...")
        
        safe_info("Subject focused session completed")

async def main():
    """Función principal para el tutor adaptativo"""
    with safe_span("main_tutor_application") as main_span:
        safe_info("Starting tutor application")
        
        print("TUTOR ADAPTATIVO - MODOS DISPONIBLES:")
        print("="*50)
        print("1. Sesión completa interactiva")
        print("2. Demo rápida")
        print("3. Demo sesión enfocada por materia")
        
        mode = get_user_input("\nElige modo (1-3): ")
        
        if LOGFIRE_ENABLED and main_span:
            main_span.set_attribute("selected_mode", mode)
        
        safe_info("Mode selected", mode=mode)
        
        if mode == "1":
            await tutor_session()
        elif mode == "2":
            await quick_tutor_demo()
        elif mode == "3":
            await subject_focused_session()
        else:
            print("Opción inválida")
            safe_warning("Invalid mode selected", mode=mode)
        
        safe_info("Tutor application completed")

if __name__ == '__main__':
    asyncio.run(main())