import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Get API Key from Streamlit Secrets
# --------------------------------------------------

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is missing from Streamlit Secrets."
    )


# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(
    api_key=GOOGLE_API_KEY
)


# --------------------------------------------------
# Gemini Model
# --------------------------------------------------

MODEL_NAME = st.secrets.get(
    "GEMINI_MODEL",
    "gemini-flash-latest"
)


# --------------------------------------------------
# Ask Gemini
# --------------------------------------------------

def ask_gemini(question, context=""):

    prompt = f"""
You are an expert Business Intelligence Analyst.

You are helping users analyze business sales data.

Answer ONLY using the supplied sales records.

==============================
SALES DATA
==============================

{context}

==============================
USER QUESTION
==============================

{question}

==============================
INSTRUCTIONS
==============================

1. Give a direct answer.
2. Explain the business insights.
3. Provide 3 actionable recommendations.
4. If the answer is not available in the provided data, clearly say:

"I couldn't find enough information in the uploaded sales data."

5. Never make up facts.

Respond professionally using Markdown.
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            # --------------------------------------
            # Check response
            # --------------------------------------

            if response is None:
                return "❌ Gemini returned None."

            if not hasattr(response, "text"):
                return (
                    "❌ Gemini response does not contain text.\n\n"
                    f"Response type: {type(response)}"
                )

            if not response.text:
                return "❌ Gemini returned an empty response."

            return response.text

        except Exception as e:

            error_type = type(e).__name__
            error_message = str(e)

            # --------------------------------------
            # Rate limit / temporary error
            # --------------------------------------

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
            ):

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt
                    time.sleep(wait_time)

                    continue

                return (
                    "⚠️ Gemini is temporarily unavailable.\n\n"
                    "Please try again in a few minutes."
                )

            # --------------------------------------
            # Invalid model
            # --------------------------------------

            if "404" in error_message:

                return (
                    f"❌ Gemini model '{MODEL_NAME}' was not found.\n\n"
                    "Check GEMINI_MODEL in Streamlit Secrets."
                )

            # --------------------------------------
            # Invalid API key
            # --------------------------------------

            if (
                "401" in error_message
                or "403" in error_message
                or "API_KEY_INVALID" in error_message
            ):

                return (
                    "❌ Google API key is invalid.\n\n"
                    "Please check GOOGLE_API_KEY in Streamlit Secrets."
                )

            # --------------------------------------
            # Any other error
            # --------------------------------------

            return (
                f"❌ Gemini Error\n\n"
                f"**Error Type:** `{error_type}`\n\n"
                f"**Message:** `{error_message}`"
            )

    return "❌ Unable to generate a Gemini response."


# --------------------------------------------------
# Simple Gemini
# --------------------------------------------------

def ask_gemini_simple(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response is None:
            return "❌ Gemini returned None."

        if not hasattr(response, "text"):
            return (
                "❌ Gemini response does not contain text.\n\n"
                f"Response type: {type(response)}"
            )

        if not response.text:
            return "❌ Gemini returned an empty response."

        return response.text

    except Exception as e:

        return (
            f"❌ Gemini Error\n\n"
            f"**Error Type:** `{type(e).__name__}`\n\n"
            f"**Message:** `{str(e)}`"
        )