import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def detect_intent(question):

    prompt = f"""
You are an AI query classifier.

Return ONLY valid JSON.

Supported intents:

highest_sales_category

highest_profit_region

sales_by_segment

monthly_sales

top_products

If question doesn't match:

unknown

Question:

{question}

Output format:

{{
 "intent":"..."
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return json.loads(response.text)["intent"]