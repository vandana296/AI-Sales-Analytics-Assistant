import os
import time

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


# --------------------------------------------------
# Ask Gemini
# --------------------------------------------------

def ask_gemini(question, context=""):

    prompt = f"""
You are an expert Business Intelligence Analyst.

You are helping users analyze business sales data.

Answer ONLY using the supplied sales records.

==================================================

SALES DATA

{context}

==================================================

USER QUESTION

{question}

==================================================

Instructions:

1. Give a direct answer.
2. Explain the business insights.
3. Provide 3 actionable recommendations.
4. If the answer is not available in the provided data, clearly say:
   "I couldn't find enough information in the uploaded sales data."
5. Never make up facts.

Respond professionally using Markdown.
"""

    max_retries = 5

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if (
                response is not None
                and hasattr(response, "text")
                and response.text
            ):
                return response.text

            return "⚠️ Gemini returned an empty response."

        except Exception as e:

            error = str(e)

            # Temporary overload
            if "503" in error or "UNAVAILABLE" in error:

                if attempt < max_retries - 1:

                    wait = 2 ** attempt

                    time.sleep(wait)

                    continue

                return (
                    "⚠️ Gemini AI is currently experiencing high demand.\n\n"
                    "Please try again in a few minutes."
                )

            # Invalid model
            elif "404" in error:

                return (
                    f"❌ Model '{MODEL_NAME}' was not found.\n"
                    "Please check the GEMINI_MODEL value in your .env file."
                )

            # Invalid API Key
            elif "401" in error or "403" in error:

                return (
                    "❌ Invalid Google API Key.\n"
                    "Please verify GOOGLE_API_KEY in your .env file."
                )

            else:

                return f"❌ AI Error:\n\n{error}"

    return "❌ Unable to generate a response."

# --------------------------------------------------
# Simple Gemini (No RAG Context)
# --------------------------------------------------

def ask_gemini_simple(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if (
            response is not None
            and hasattr(response, "text")
            and response.text
        ):
            return response.text

        return "⚠️ Gemini returned an empty response."

    except Exception as e:

        return f"❌ AI Error:\n\n{e}"