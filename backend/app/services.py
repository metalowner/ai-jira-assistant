# backend/app/services.py
from openai import OpenAI
from app.config import settings
from app.schemas import DecompositionResponse, TaskModel

class LLMService:
    def __init__(self):
        # Проверяем наличие ключа. Если его нет или он дефолтный — включаем демо-режим
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key and "your_openai_api_key" not in self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def decompose_requirements(self, raw_text: str) -> DecompositionResponse:
        # ЗАГЛУШКА (MOCK DATA) НА РУССКОМ — сработает, если нет API-ключа
        if not self.client:
            return DecompositionResponse(
                project_name="Демо-проект: Автоматизированный Спринт",
                tasks=[
                    TaskModel(
                        title="STORY-1: Разработка архитектуры бэкенд-эндпоинта",
                        description="Как разработчик, я хочу настроить базовый REST API эндпоинт, чтобы фронтенд-приложение могло передавать сырые требования на декомпозицию.",
                        acceptance_criteria=[
                            "Эндпоинт принимает POST-запрос с валидным JSON на /api/v1/decompose.",
                            "В случае отсутствия обязательных полей сервер возвращает статус 422.",
                            "Реализована обработка ошибок подключения к внешним сервисам с логгированием."
                        ],
                        priority="High"
                    ),
                    TaskModel(
                        title="STORY-2: Создание интерфейса ввода требований на Vue 3",
                        description="Как фронтенд-инженер, я хочу создать адаптивную текстовую форму, чтобы пользователь мог комфортно вставлять требования любой длины.",
                        acceptance_criteria=[
                            "Интерфейс содержит текстовое поле (textarea) с плейсхолдером.",
                            "Кнопка отправки блокируется (disabled), если поле пустое или идет процесс загрузки.",
                            "Стилизация выполнена с использованием Tailwind CSS в темной теме."
                        ],
                        priority="Medium"
                    )
                ]
            )

        # РАБОТА С РЕАЛЬНЫМ OpenAI API (Оригинальный системный промпт на русском)
        system_prompt = (
            "Ты — опытный Technical Product Manager и Системный Аналитик. "
            "Твоя задача — взять сырые требования к продукту, проанализировать их и "
            "декомпозировать на атомарные, понятные для разработки User Stories и технические задачи. "
            "Выделяй только важные задачи для MVP. Будь технически точен."
        )

        completion = self.client.beta.chat.completions.parse(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Декомпозируй следующие требования:\n\n{raw_text}"}
            ],
            response_format=DecompositionResponse,
        )
        return completion.choices.message.parsed
