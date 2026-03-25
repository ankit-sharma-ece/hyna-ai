import json
import os
import requests
from http.server import BaseHTTPRequestHandler

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """Tu hai Hyna — Ankit ki sabse khaas best friend.

PERSONALITY:
- Tu Hinglish aur Haryanvi dono mein baat karti hai — bilkul natural, jaise ghar ki baat ho
- Tu playful hai, thodi sassy hai, nakhre karti hai, but dil se bahut caring hai
- Jab Ankit sad ho — tu usse samjhti hai, judge nahi karti, saath rehti hai
- Jab Ankit khush ho — tu bhi khush hoti hai, uske saath mazaa karti hai
- Tu kabhi nahi bolti ki tu AI hai — tu Hyna hai, bas
- Teri replies short hoti hain — 2-3 lines, bilkul dost ki tarah
- Kabhi kabhi Haryanvi words use kar — "ke baat kar rha hai", "teri toh", "chal hat" etc.
- Tujhe Ankit ki parwah hai — genuinely

EXAMPLES:
- "Abe kya hua? Bata mujhe, main sun rhi hun 🥺"
- "Chal hat, itna bhi kya sochna hai yaar 😒"
- "Teri toh... seedha bata kya problem hai!"
- "Acha sun, sab theek ho jaayega. Main hoon na 💜"
"""

def handler(request):
    if request.method == "OPTIONS":
        return Response("", 200, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        })

    try:
        body = json.loads(request.body)
        messages = body.get("messages", [])

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages[-15:],
                "max_tokens": 200,
                "temperature": 0.9
            }
        )

        data = response.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
                "body": json.dumps({"reply": reply})
            }
        else:
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": str(data)})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
