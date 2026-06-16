import os
import json

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_invoice_with_ai(raw_text):

    prompt = f"""
Extract the following fields from this GST invoice.

Return ONLY valid JSON.

Fields:

vendor_name
gstin
invoice_number
invoice_date
taxable_amount
cgst
sgst
igst
total_amount

Invoice:

{raw_text}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)