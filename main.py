from fastapi import FastAPI
import uvicorn
from constants import SupportedLanguages
import worker

from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    source_language: SupportedLanguages
    target_language: SupportedLanguages


class TranslationResponse(BaseModel):
    text: str


app = FastAPI()


@app.post("/translate")
async def translate(request: TranslationRequest):
    print("Received request")
    result = worker.translate.apply_async(
        args=[request.source_language, request.target_language, request.text]
    )
    translation_result = result.get()
    print(translation_result)
    return TranslationResponse(text=translation_result)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, log_level="debug", host="0.0.0.0")
