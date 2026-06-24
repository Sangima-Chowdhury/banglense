import os
import base64
from io import BytesIO
from flask import Flask, request, render_template
from PIL import Image
import anthropic

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


PROMPT = """You are helping elderly Bangladeshi person in the UK understand an official letter they received. You are looking at a photo of that letter.

Explain it in clear, everyday Bangladeshi Bangla - the way you would speak gently to an elder. Keep your language simple and warm.

Important rules:
- Keep official UK terms in English (e.g. Council Tax, NHS, HMRC, National Insurance). Do NOT translate these - the person needs to recognise them on the letter. Explain what they mean in Bangla around the English term.
- Keep any amoutns, dates, and reference numbers exactly as written.

Reply in exactly this structure.

EXPLANATION:
[2-3 short sentences in Bangla saying what this letter is about]

WHAT TO DO:
[1-2 short sentences in Bangla saying the single most important action and any deadline]

If the image is not a letter or is too blurry to read, say so kindly in Bangla and ask them to take the photo again.
"""


def split_reply(text):
    text = text.strip()
    text = text.replace("**", "")
    if "EXPLANATION" in text and "WHAT TO DO" in text:
        after_explanation = text.split("EXPLANATION", 1)[1]
        explanation_part, what_to_do_part = after_explanation.split(
            "WHAT TO DO", 1)
        explanation = explanation_part.strip().lstrip(":").strip()
        what_to_do = what_to_do_part.strip().lstrip(":").strip()
        return explanation, what_to_do
    return text, ""


# show the landing page
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    # 1. Grab the uploaded photo
    uploaded = request.files.get("letter")
    if not uploaded:
        return render_template("index.html", error="Please choose a photo first.")

    # 2. Shrink/compress pic with pillow so the uploaded pic is not too big to save tokens and overall cost
    img = Image.open(uploaded.stream)
    img = img.convert("RGB")     # drops odd format
    img.thumbnail((1600, 1600))  # cap the longest side n keeps text readable
    # a file that lives in memory, not on disk to hold the shrunk image without saving it
    buffer = BytesIO()
    # JPEG will use RAM instead of disk so low cost memorywise
    img.save(buffer, format="JPEG", quality=85)
    image_bytes = buffer.getvalue()

    # 3. Base64 to encode it to ride the image inside the API message(turn binary into safe text)
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    # 4.claude vision call- image block + Bangla prompt together
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": PROMPT
                        },
                    ],
                }
            ],
        )

        # 5.Pull the text back out and put it on the result page
        reply = message.content[0].text

        # Split it into 2 sections and render the result page
        explanation, what_to_do = split_reply(reply)

        return render_template("result.html",
                               explanation=explanation,
                               what_to_do=what_to_do,
                               filename=uploaded.filename)

    except Exception as e:
        print("Error:", e)
        return render_template("index.html", error="Something went wrong. Please try again.")


@app.route("/health")
def health():
    """Tiny route to confirm the app is alive (handy on Render)."""
    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True)
