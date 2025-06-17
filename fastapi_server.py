from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import json

app = FastAPI()

# Pydantic model for request validation
class ProductRequest(BaseModel):
    amount: float
    category: str

# Endpoint to generate a product using Ollama
@app.post("/generate_product")
async def generate_product(request: ProductRequest):
    try:
        prompt = f"""
        Generate a name of a product that can be sold online in the {request.category} category.
        Rules:
        - Use title case.
        - No punctuation.
        - No parentheses, dashes, or dollar signs.
        - No amounts or numbers as words.
        - Use simple phrases.
        - Examples: 'LED Light Bulbs', 'Bath Towel'
        Additionally, provide a brief description (up to 50 characters) of the product.
        Return the output as a JSON object with 'product_name' and 'description' fields, wrapped in triple backticks (```json\n{{}}\n```).
        Example:
        ```json
        {{
            "product_name": "LED Light Bulbs",
            "description": "Bright energy saving lights"
        }}
        """
        response = ollama.generate(
            model='mistral:7b-instruct-v0.3-q4_0',
            prompt=prompt,
            options={"temperature": 0.8}
        )
        raw_response = response['response'].strip()
        if not raw_response:
            raise ValueError("Empty response from Ollama")
        if raw_response.startswith('```json'):
            raw_response = raw_response[7:].split('```', 1)[0].strip()
        result = json.loads(raw_response)
        if 'product_name' not in result or 'description' not in result:
            raise ValueError("Missing 'product_name' or 'description' key")
        result['description'] = result['description'][:50]  # Truncate description
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating product: {str(e)}")

# Run the server: uvicorn fastapi_server:app --host 0.0.0.0 --port 8000