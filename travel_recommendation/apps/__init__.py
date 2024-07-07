from fastapi import APIRouter
from apps.provider.llm_provider import *
import pandas as pd

router = APIRouter(prefix="/destination", tags=['Destination'])

@router.get("/{query}")
async def get_destination(query: str):
    question_tags = get_question_tags(query)
    destination_name = get_destinations(question_tags)
    return destination_name

@router.get("/data/")
async def get_data():
    df = pd.read_excel("destination_1.xlsx")
    df = df.to_dict(orient='records')
    return df