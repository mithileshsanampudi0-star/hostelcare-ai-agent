import base64
from groq import Groq
from config import GROQ_API_KEY, GROQ_VISION_MODEL

client = Groq(api_key=GROQ_API_KEY)

VISION_PROMPT = (
    "You are looking at a photo of a hostel maintenance issue. Describe concisely "
    "what is wrong (e.g. leaking pipe, broken switch, damaged furniture, mold, "
    "cracked wall), and mention any visible room number, severity, or safety "
    "concern. Keep it to 2-3 sentences."
)


def describe_image(image_bytes, mime_type="image/jpeg"):
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64}"

    response = client.chat.completions.create(
        model=GROQ_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": VISION_PROMPT},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
