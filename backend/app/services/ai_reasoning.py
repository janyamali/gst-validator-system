import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

print(
    "Gemini Key Found:",
    bool(os.getenv("GEMINI_API_KEY"))
)

print(
    "Gemini Key Found:",
    bool(os.getenv("GEMINI_API_KEY"))
)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


def generate_reason(
    validation_result,
    match_result,
    duplicate_detected,
    final_status
):

    prompt = f"""
You are a GST audit assistant.

Validation Status:
{final_status}

Validation Result:
{validation_result}

Claim Match Result:
{match_result}

Duplicate Detected:
{duplicate_detected}

Explain in simple business language
why the claim is VALID or INVALID.

Keep response under 80 words.
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(
            "Gemini Error:",
            e
        )

        return (
            "AI explanation unavailable. "
            "Validation completed using rule-based engine."
        )