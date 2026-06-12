import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
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

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:

        print("Groq Error:", e)

        return (
            "AI explanation unavailable. "
            "Validation completed using rule-based engine."
        )