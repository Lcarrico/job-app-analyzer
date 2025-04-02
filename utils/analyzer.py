import json
import re
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

def extract_json_block(text):
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text.strip())
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("No valid JSON block found.")

def analyze_texts_as_json(api_key, resume, cover_letter, job_description):
    client = OpenAI(api_key=api_key)

    resume_prompt = f"""
You are a job application evaluator. Compare the RESUME to the JOB DESCRIPTION and return a structured JSON object with the following format:

{{
  "all_items_required": {{
    "required_experience": [...],
    "education": [...],
    "certifications": [...],
    "hard_skills": [...],
    "soft_skills": [...],
    "culture_keywords": [...]
  }},
  "skills_match": {{
    "required_experience": [...],
    "education": [...],
    "certifications": [...],
    "hard_skills": [...],
    "soft_skills": [...],
    "culture_keywords": [...]
  }}
}}

Instructions:
- For `all_items_required`, list each requirement exactly as written in the job description.
- For `skills_match`, include an item only if it appears in the resume, but use the exact text from `all_items_required` — do not reword or paraphrase.
- This means: if the resume implies or describes the skill, it's a match — but always copy the exact phrase from `all_items_required` into `skills_match`.

Only return valid JSON. Do not include markdown formatting or explanations.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
"""

    cover_prompt = f"""
You are a professional hiring evaluator. Analyze the COVER LETTER in the context of the JOB DESCRIPTION and return a JSON rubric with 5 scoring categories. Each category is worth up to 20 points, totaling 100.

Use the defined scoring tiers and checklist items for each category below. Base the score on how many of the listed traits are clearly and effectively demonstrated in the letter. Only assign higher scores when a higher number of traits are present and executed at an exceptional level.

---

### SCORING FORMAT:
Return the result as valid JSON in this format:

{{
  "rubric": {{
    "hook_strength": {{ "score": 0-20, "reason": "..." }},
    "uniqueness": {{ "score": 0-20, "reason": "..." }},
    "engagement": {{ "score": 0-20, "reason": "..." }},
    "culture_alignment": {{ "score": 0-20, "reason": "..." }},
    "additional_value": {{ "score": 0-20, "reason": "..." }}
  }}
}}

---

### CATEGORY SCORING SYSTEM:

For each category below:

- **0 points** → 0–1 traits demonstrated
- **1–5 points** → 2–3 traits demonstrated
- **5–10 points** → All traits demonstrated
- **11–15 points** → All traits demonstrated with polish and strong structure
- **16–20 points** → All traits demonstrated with excellence and originality — goes beyond expectations or includes a "genius" insight or moment

---

### 1. Hook Strength (Intro Opening)

Checklist:
- Opens with a fresh, original sentence — not a template or generic opening  
- Instantly establishes a personal connection to the company’s mission, product, or values  
- Introduces a narrative thread or insight that carries through the letter  
- Feels like the beginning of a compelling story, not just an application  

---

### 2. Uniqueness / Personal Brand

Checklist:
- Shares a distinct point of view, personal philosophy, or rare experience  
- Clearly articulates why they are uniquely suited to this role — not just qualified  
- Tells a short, meaningful story or origin moment that connects to the work  
- Voice feels authentic, intentional, and undeniably theirs  

---

### 3. Engagement / Writing Quality

Checklist:
- Language is rhythmic, vivid, and precise — avoids corporate jargon or filler  
- Every sentence feels intentional — no wasted words  
- Shows emotional intelligence through tone and phrasing  
- Maintains strong pacing and energy from beginning to end  

---

### 4. Culture Alignment

Checklist:
- References the company’s actual values, tone, or brand language  
- Mirrors the company’s communication style and language choices  
- Connects their own work habits, motivations, or mindset to the company’s environment  
- Shows insight into the company’s mission, tone, or way of working — beyond surface-level language  

---

### 5. Additional Value or Strengths

Checklist:
- Mentions rare or bonus skills, experiences, or results  
- Frames value-adds in a way that solves real problems or enhances the team  
- Offers insight or perspective that expands the role or vision  
- Shows they’re thinking beyond the job description, like a partner or builder  

---

Only return valid JSON. Do not include markdown, bullet points, section headers, or any explanation outside the JSON object.

COVER LETTER:
{cover_letter}

JOB DESCRIPTION:
{job_description}
"""



    try:
        logger.info("Sending resume prompt to GPT-4o...")
        resume_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": resume_prompt}],
            temperature=0.3
        )
        resume_raw = resume_resp.choices[0].message.content.strip()
        logger.debug(f"Raw Resume GPT Response:\n{resume_raw}")
        resume_json = json.loads(extract_json_block(resume_raw))

        logger.info("Sending cover letter prompt to GPT-4o...")
        cover_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": cover_prompt}],
            temperature=0.3
        )
        cover_raw = cover_resp.choices[0].message.content.strip()
        logger.debug(f"Raw Cover Letter GPT Response:\n{cover_raw}")
        cover_json = json.loads(extract_json_block(cover_raw))

        return resume_json, cover_json

    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parsing failed: {e}")
        return {"error": f"JSON parsing failed: {e}"}, {}

    except Exception as e:
        logger.exception("❌ Unhandled exception.")
        return {"error": str(e)}, {}
