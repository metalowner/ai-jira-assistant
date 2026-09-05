from pydantic import BaseModel, Field
from typing import List, Literal

class TaskModel(BaseModel):
    title: str = Field(..., description="Краткое и понятное название задачи (Action-oriented)")
    description: str = Field(..., description="Описание по шаблону: Как [роль], я хочу [действие], чтобы [ценность]")
    acceptance_criteria: List[str] = Field(
        ..., 
        description="Критерии приемки в формате чек-листа или Definition of Done (желательно Given/When/Then)"
    )
    priority: Literal["Low", "Medium", "High"] = Field(..., description="Приоритет задачи на основе критичности фичи")

class DecompositionResponse(BaseModel):
    project_name: str = Field(..., description="Предложенное кодовое имя для эпика/проекта")
    tasks: List[TaskModel] = Field(..., description="Список декомпозированных задач для спринта")

class DecompositionRequest(BaseModel):
    raw_requirements: str = Field(..., min_length=10, description="Сырые бизнес или технические требования от пользователя")
