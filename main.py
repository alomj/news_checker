from fastapi import FastAPI, status
from config import settings
from services.openai_client import OpenAiService
from llm.query_generator import QueryGenerator
from schema import Request

app = FastAPI(title=settings.app_title,
              description=settings.app_description
              )


@app.post('/generate-news', status_code=status.HTTP_201_CREATED)
async def generate_news(request: Request):
    client = OpenAiService()
    generator = QueryGenerator(client)
    query = await generator.generate(headline=request.headline)

    return query
