from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

class ChatInput(BaseModel):
    message: str

qa_dict = {
    "el esmalte de uñas no seca y se levanta rápido": "¡Esto puede deberse a humedad, falta de preparado de la uña o esmalte de baja calidad! Mira esta guía: https://youtu.be/Vrw0PDAf_RI?si=rkm9ln-A92UkD9lK",
}

@app.post("/chat")
async def chat(input: ChatInput):
    question = input.message.lower()
    answer = qa_dict.get(question)
    if not answer:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada.")
    return {"answer": answer}
