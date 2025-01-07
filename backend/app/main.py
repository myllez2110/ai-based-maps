from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.groq_service import process_groq_query
from services.scraping_service import scrape_data
from services.geojson_converter import to_geojson

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-map/")
async def generate_map(request: PromptRequest):
    try:
        prompt = request.prompt

        groq_data = process_groq_query(prompt)
        if groq_data:
            geojson = to_geojson(groq_data)
            return geojson

        scraped_data = scrape_data(prompt)
        if scraped_data:
            geojson = to_geojson(scraped_data)
            return geojson

        raise HTTPException(status_code=404, detail="No found data for the prompt.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
