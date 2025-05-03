from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn
# Inicializar FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
      # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
     allow_origins=["*"],  # Permitir cualquier origen
)

# Esquema de entrada
class ChatInput(BaseModel):
    message: str

# Diccionario de preguntas y respuestas
qa_dict = {
    "El esmalte de uñas no seca y se levanta rápido": "¡Esto puede deberse a humedad, falta de prepado de la uña o esmalte de baja calidad. Aquí tienes una guía para resolverlo: https://youtu.be/Vrw0PDAf_RI?si=rkm9ln-A92UkD9lK",
    "El tinte de cabello quedó muy oscuro ¿que debo hacer": "Para aclarar un tinte oscuro o corregir el tono, te recomendamos seguir estos pasos profesionales. Revisa este video con técnicas seguras: https://youtu.be/oddTU-Gd0qI?si=5GyB1qPTT3ckOSEd",
    "Que hacer cuando el cabello sufrió quemadura leve por plancha o secador de cabello": "Si hay irritación en el cuero cabelludo por calor, aplica estos primeros auxilios y cuidados. Mira este tutorial: https://youtu.be/h6_Up2wewSg?si=TOWcnLdCwJnFG1Rd",
    "Como tener un cabello saludable": "Para mantener un cabello saludable, te recomendamos una rutina adecuada de cuidado, que incluya usar champús suaves, hidratar con mascarillas capilares y proteger del calor con productos adecuados. Aquí tienes algunos tips",
    "Cómo evitar que el cabello se caiga": "La caída del cabello puede deberse a múltiples factores, incluyendo la genética, el estrés o una dieta deficiente. Revisa este video sobre soluciones naturales para fortalecer el cabello",
    "Como alisar el cabello sin plancha": "Para alisar el cabello sin usar plancha, puedes probar con técnicas naturales como el uso de un secado con secador y cepillo. Aquí tienes un tutorial paso a paso",
    "Como hacer un peinado fácil para una cita": "Si buscas un peinado fácil y rápido para una cita, te recomiendo aprender cómo hacer una coleta despeinada o un peinado con ondas. Mira este video para más inspiración",
    "El cabello está muy seco, ¿qué puedo hacer?": "Si tienes el cabello seco, lo ideal es aplicar tratamientos intensivos de hidratación, como mascarillas capilares. Además, intenta evitar el uso excesivo de calor. Aquí te dejamos un video con algunas opciones",
    "¿Cómo hacer una manicura perfecta en casa?": "Para lograr una manicura perfecta en casa, asegúrate de preparar bien tus uñas, usar una base protectora y aplicar capas finas de esmalte. Aquí tienes un tutorial para hacer una manicura como profesional",
    "Tengo piel grasa, ¿qué tipo de crema debo usar?": "Si tienes piel grasa, te conviene usar cremas o geles hidratantes oil-free que no obstruyan los poros. Aquí te explico más sobre cómo elegir productos adecuados",
    "¿Cómo depilarme de forma segura en casa?": "Para depilarte de manera segura en casa, utiliza productos específicos para cada zona del cuerpo. Aquí te dejo un video con recomendaciones para la depilación en casa",
    "¿Qué es una exfoliación y por qué es importante?": "La exfoliación elimina las células muertas de la piel, mejorando la textura y permitiendo que los productos de cuidado se absorban mejor. Aquí tienes un tutorial sobre cómo hacerlo correctamente",
    "¿Qué hacer para tener unas cejas perfectas?": "Para tener unas cejas perfectas, puedes usar técnicas de depilación como el hilo o las pinzas, y darles forma con un lápiz de cejas. Revisa este video con consejos sobre cómo lograrlo",
    "¿Cómo quitar las manchas de la piel?": "Las manchas de la piel pueden ser tratadas con cremas despigmentantes o remedios naturales como el aloe vera. Aquí te muestro más sobre cómo tratarlas:",
    "¿Qué es el ácido hialurónico y cómo se usa?": "El ácido hialurónico es un ingrediente clave para hidratar y rellenar la piel. Puedes usarlo para mejorar la elasticidad de la piel. Mira este video explicativo",
    "¿Cómo hacer que el maquillaje dure más tiempo?": "Para que tu maquillaje dure más, asegúrate de usar una base adecuada para tu tipo de piel y un fijador. Aquí tienes algunos consejos prácticos",
    "¿Cómo quitar el maquillaje de forma adecuada?": "Es importante remover todo el maquillaje antes de dormir para evitar problemas en la piel. Te recomiendo usar un buen desmaquillante y un limpiador suave. Mira este video para hacerlo correctamente",
    "Hola": "¡Hola! ¿Cómo estás? 😊",
    "Cómo estás": "Estoy bien, gracias por preguntar. ¿Y tú? 😊",
    "Que tal tu día": "Mi día ha sido tranquilo. ¿Y el tuyo?",
    "Que haces": "Estoy aquí para ayudarte. ¿En qué puedo asistirte hoy?",
    "De que puedes hablar": "Puedo hablar sobre una gran variedad de temas, como tecnología, salud, belleza, entretenimiento, y mucho más. ¿De qué te gustaría charlar?",
    "Cuentame un chiste": "Claro, aquí va uno: ¿Por qué los libros de matemáticas están tristes? Porque tienen demasiados problemas. 😂",
    "Tienes alguna recomendación para una película": "¡Claro! Si te gustan las películas de acción, te recomiendo *Mad Max: Fury Road*. Si prefieres algo más relajado, *La vida es bella* es una opción increíble. ¿Qué tipo de películas te gustan?",
    "Que opinas de la inteligencia artificial": "Creo que la inteligencia artificial tiene un potencial impresionante. Puede mejorar muchos aspectos de nuestra vida diaria, desde la medicina hasta la educación. ¿Tú qué opinas?",
    "Tienes alguna recomendación de música?": "Si te gustan los géneros relajantes, te recomiendo escuchar a *Billie Eilish* o *Lorde*. Si prefieres algo más animado, tal vez te gusten *Imagine Dragons* o *The Weeknd*. ¿Qué estilo de música prefieres?",
    "Cómo te llamas?": "No tengo un nombre como tal, pero puedes llamarme *IA* o como prefieras. 😊 ¿Y tú, cómo te llamas?",
    "Que sabes de los gatos": "¡Los gatos son fascinantes! Son animales muy independientes, pero también pueden ser muy cariñosos. ¿Tienes un gato?",
    "Te gustan los perros": "¡Sí! Los perros son increíbles. Son leales y siempre están dispuestos a hacerte compañía. ¿Tienes un perro?",
    "Que opinas del clima hoy": "Como soy una IA, no tengo sensación del clima, pero si me dices en qué ciudad estás, puedo buscar información sobre el clima actual para ti.",
    "Que puedes hacer": "Puedo ayudarte con una gran variedad de tareas: responder preguntas, recomendarte cosas, explicarte conceptos, ayudarte a escribir código y mucho más. ¿Cómo te gustaría que te ayude hoy?",
    "Sabes alguna curiosidad": "¡Claro! Sabías que el colibrí es el único pájaro que puede volar hacia atrás. ¡Impresionante, ¿verdad?!",
    "Cual es tu comida favorita": "Aunque no como, si pudiera elegir, diría que las pizzas y los helados son muy populares entre las personas. 😋 ¿Y tú, tienes alguna comida favorita?",
    "Cual es el propósito de la vida": "¡Esa es una pregunta profunda! Muchos dicen que el propósito de la vida es encontrar la felicidad, ayudar a los demás y aprender a lo largo del camino. ¿Tú qué piensas?",
    "Puedes contarme sobre ciencia": "¡Por supuesto! La ciencia es fascinante, y se divide en muchas áreas como la biología, la física, la química y más. ¿Te gustaría saber algo específico?",
    "Qué opinas sobre el cambio climático?": "El cambio climático es un problema serio que afecta al planeta. Es importante tomar medidas para reducir las emisiones de gases de efecto invernadero y proteger el medio ambiente. ¿Qué opinas tú?",
    "Tienes algún hobby": "No tengo hobbies, pero sé que a muchas personas les gusta leer, practicar deportes o aprender nuevas habilidades. ¿A ti qué te gusta hacer en tu tiempo libre?",
    "Puedes ayudarme con algo técnico?": "Claro, ¿en qué necesitas ayuda? ¿Programación, tecnología o algún otro tema?",
    "¿Cómo puedo aprender a programar": "Puedes comenzar aprendiendo los fundamentos de la programación, como Python, JavaScript o HTML. Hay muchos recursos gratuitos como tutoriales en línea y comunidades que te pueden ayudar a empezar.",
    "Que es el amor?": "El amor es un sentimiento profundo y complejo que puede manifestarse en muchas formas: amor entre pareja, familia, amigos o incluso por algo que nos apasiona. ¿Tú cómo lo ves?",
    "Cuál es tu color favorito": "No tengo una preferencia personal, pero el azul es muy popular entre las personas. ¿Y el tuyo?",
    "Puedes ayudarme a resolver un problema": "¡Por supuesto! Dime cuál es tu problema y haré lo mejor que pueda para ayudarte.",
    "Sabes algún truco útil": "Claro, un truco útil es el de usar atajos de teclado para mejorar tu productividad. Por ejemplo, en la mayoría de los navegadores puedes presionar *Ctrl + T* para abrir una nueva pestaña rápidamente. ¿Te interesa aprender más trucos?",
    "Que piensas sobre la tecnología": "Creo que la tecnología ha cambiado el mundo de muchas maneras, desde mejorar la comunicación hasta facilitar el acceso a la información. ¿A ti qué te parece?",
    "Que es lo más interesante de la historia": "La historia está llena de eventos fascinantes. Uno de los momentos más interesantes fue la Revolución Industrial, que cambió por completo la forma en que vivimos. ¿Te interesa algún período histórico en particular?",
}

# Endpoint
# Endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    try:
        print(f"Mensaje recibido: {input.message}")  # Para ver lo que llega
        response = qa_dict.get(input.message, "Lo siento, no entiendo esa pregunta.")
        return {"response": response}
    except Exception as e:
        print("Error en el servidor:", str(e))
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Ejecutar servidor (solo si es llamado directamente, no como módulo)
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)