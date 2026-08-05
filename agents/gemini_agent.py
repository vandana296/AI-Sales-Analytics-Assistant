import os

from dotenv import load_dotenv
from google import genai
from utils.logger import logger

from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(result_df, question):

    data = result_df.to_markdown(index=False)

    prompt = f"""
{SYSTEM_PROMPT}

Business Data

{data}

User Question

{question}

Answer like a Senior Business Analyst.

Give:

1. Summary

2. Important Findings

3. Business Recommendation
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text