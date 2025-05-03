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
    # ... (más preguntas y respuestas)
}

# Endpoint para recibir preguntas y dar respuestas
@app.post("/chat")
async def chat(input: ChatInput):
    question = input.message
    answer = qa_dict.get(question.lower())
    
    if not answer:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada.")
    
    return {"answer": answer}

# Iniciar servidor solo si el script es ejecutado directamente
if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.environ.get("PORT", 8000))) 
