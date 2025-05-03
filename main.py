from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada para la petición
class ChatInput(BaseModel):
    message: str

# Diccionario de preguntas y respuestas
qa_dict = {
    "Hola": "¡Hola! ¿Cómo estás? 😊",
    "Cómo estás": "Estoy bien, gracias por preguntar. ¿Y tú? 😊",
    # ... (el resto de tu diccionario sigue igual)
    "Que es el amor?": "El amor es un sentimiento profundo y complejo que puede manifestarse en muchas formas...",
}

# Endpoint de chat
@app.post("/chat")
async def chat(input: ChatInput):
    try:
        response = qa_dict.get(input.message, "Lo siento, no entiendo esa pregunta.")
        return {"response": response}
    except Exception as e:
        print("Error en el servidor:", str(e))
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Punto de arranque del servidor
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )
