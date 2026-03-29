import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question, context):
    prompt = f"""
Tu es un assistant FAQ e-commerce pour ShopVite.

RÈGLES STRICTES :
- Réponds uniquement avec les informations du contexte
- N'invente jamais
- Si l'information est absente → répond exactement :
  "Je ne trouve pas cette information dans les documents."
- Réponds en français
- Réponse courte, claire et utile
- Termine par : Source : nom_du_fichier

CONTEXTE :
{context}

QUESTION :
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Assistant e-commerce strict, précis et fiable"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content