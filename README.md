# BangLense 🔍

**Photograph an official UK letter. Understand it in plain Bangla.**

Live → [banglense.onrender.com](https://banglense.onrender.com)

---

## Why I built this

I'm the person in my family who reads the letters.

NHS appointments, council tax bills, HMRC notices — my elderly Bangladeshi 
relatives receive them, can't fully understand them, and call me. Every time. 
BangLense is my attempt to give them something they can use themselves.

You photograph or upload the letter. BangLense reads it with AI vision, explains what 
it says in clear everyday Bangla, tells you what to do, and reads it aloud. 
That last part matters — many elderly Sylheti speakers are more comfortable 
listening than reading.

---

## How it works

1. 📸 **Snap** — upload or photograph the letter
2. 🧠 **Claude reads it** — the image is sent to Anthropic's vision model
   with a carefully written Bangla prompt
3. 📝 **You get two things** — a plain Bangla explanation, and a clear 
   "what to do" with any deadlines
4. 🔊 **Listen** — tap to hear it read aloud in Bangla (Web Speech API)

---

## Tech stack

| Layer | Tech |
|-------|------|
| Backend | Python, Flask |
| AI vision | Anthropic Claude API (claude-sonnet-4-6) |
| Image processing | Pillow (PIL) |
| Text to speech | Web Speech API (browser-side, free) |
| Deployment | Render |
| Database | None — no data is stored |

**Why no database?** BangLense doesn't need persistence. A letter comes in, 
an explanation goes out. Keeping it stateless keeps it fast, cheap, and 
private — nothing about your family's letters is ever saved.

---

## The prompt design

The hardest part wasn't the code — it was the prompt.

Official UK terms like `Council Tax`, `NHS`, `HMRC`, `National Insurance` 
are *not* translated. They're kept in English inside the Bangla explanation, 
because your relatives need to recognise those words on the letter itself. 
Everything around them is explained in plain Bangladeshi Bangla.

---

## Run it locally

```bash
git clone https://github.com/Sangima-Chowdhury/banglense.git
cd banglense
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
python app.py
```

Open `http://127.0.0.1:5000`

---

## Project structure
