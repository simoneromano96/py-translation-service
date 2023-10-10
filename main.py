from fastapi import FastAPI
from constants import SupportedLanguages
import worker

from pydantic import BaseModel


class TranslateRequest(BaseModel):
    text: str
    source_language: SupportedLanguages
    target_language: SupportedLanguages


class TranslationResponse(BaseModel):
    text: str


app = FastAPI()


@app.post("/translate")
async def translate(request: TranslateRequest):
    result = worker.translate.apply_async(
        args=[request.source_language, request.target_language, request.text]
    )
    translation_result = result.get()
    return TranslationResponse(text=translation_result)
