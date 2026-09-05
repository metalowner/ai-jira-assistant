from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import DecompositionRequest, DecompositionResponse
from app.services import LLMService

app = FastAPI(
    title="AI-Driven Jira/Linear Assistant API",
    description="Микросервис для автоматической декомпозиции требований с помощью LLM",
    version="1.0.0"
)

# Настраиваем CORS, чтобы наш будущий фронтенд на Vue 3 мог делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене тут должен быть конкретный урл фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/decompose", response_model=DecompositionResponse)
def decompose(payload: DecompositionRequest):
    try:
        result = llm_service.decompose_requirements(payload.raw_requirements)
        return result
    except Exception as e:
        # На гитхабе важно показать умение обрабатывать ошибки
        raise HTTPException(status_code=500, detail=f"Ошибка при работе с LLM: {str(e)}")
