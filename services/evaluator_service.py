import os, yaml, logging
from typing import List, Dict, Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image


MOCK_MODE   = False
GEMINI_KEY = "AIzaSyAz51Dt6eRLj29U-7cjq7eoBSITSKewfT8"
GEMINI_MODEL= os.getenv("GEMINI_MODEL", "models/gemini-1.5-flash-latest")

import google.generativeai as genai
genai.configure(api_key=GEMINI_KEY)

gemini = genai.GenerativeModel(GEMINI_MODEL)

with open(os.getenv("EVALUATOR_CONFIG", "config.yaml")) as f:
    cfg_raw = yaml.safe_load(f)

class Config(BaseModel):
    confidence_threshold: float
    candidate_profile: Dict[str, Any]
    cv_summary: str

cfg = Config(**cfg_raw)

def vision_yaml(img_path: str, question: str) -> dict:
    """
    Send a PIL image + prompt, return parsed YAML (or {} on error).
    """
    img = Image.open(img_path)

    resp = gemini.generate_content([img, question])
    raw  = resp.text                     # may come fenced with ```yaml
    #print("#####RAW######", raw)
    clean = raw.split("```")[-2] if "```" in raw else raw
    return raw
    
def gemini_yaml(prompt: str) -> Dict[str, Any]:
    if MOCK_MODE:
        return {}
    resp = gemini.generate_content(prompt)
    
    text = resp.text.strip().splitlines()
    #print("##########################################TEXT###################################", float(text[1].strip().split(':')[1]))
    try:
        return float(text[1].strip().split(':')[1])
    except Exception:
        return {}
    
def gemini_yaml_gen(prompt: str) -> Dict[str, Any]:
    """Send a prompt, get YAML dict back (handles mock mode)."""
    if MOCK_MODE:
        return {}
    resp = gemini.generate_content(prompt)
    
    text = resp.text.strip().splitlines()
    #rint("##########################################TEXT###################################", text)
    try:
        return yaml.safe_load(text)
    except Exception:
        return {}

app = FastAPI(
    title="Candidate Confidence Evaluator",
    description="LLM-only confidence evaluator (text, voice, image)",
    version="0.2.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

class EvaluationRequest(BaseModel):
    turn_id: str
    text_response: str
    audio_url: str
    image_urls: List[str]
    metadata: Dict[str, Any] = {}

class EvaluationResponse(BaseModel):
    turn_id: str
    confidence_score: float
    decision: str
    reasoning: str
    suggested_test: Dict[str, Any]

def analyze_text_confidence(text: str) -> float:

    prompt = f"""
Given the following interview answer, judge how confident and truthful
the candidate sounds. Reply in YAML with a single key `confidence` in 0-1.

Answer:
\"\"\"{text}\"\"\"
"""
    data = gemini_yaml(prompt)
    #print("TEXT", data.text)

    return data


from google.genai import types

async def analyze_image_confidence(image_paths: List[str]) -> float:

    if not image_paths:
        return 0.5

    scores: list[float] = []
    prompt = (
        "Assess facial emotion. "
        "Return a float between 0 (very suspicious) and 1 "
        "(very confident). Respond with only the number."
    )

    for path in image_paths:
        try:
            data = vision_yaml(path, prompt)
        except Exception as e:
            logging.warning(f"Image analysis failed for {path}: {e}")
            scores.append(0.0)

    return float(data)


@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_candidate(req: EvaluationRequest) -> EvaluationResponse:
    t_conf = analyze_text_confidence(req.text_response)
    #v_conf = await analyze_voice_confidence(req.audio_url)
    i_conf = await analyze_image_confidence(["static/face2.jpg","static/face2.jpg"])
    overall = (i_conf+t_conf)/2

    decision = (
        "needs-live-code-test"
        if overall < cfg.confidence_threshold
        else "no-test-needed"
    )

    test_json = {}
    if decision == "needs-live-code-test":
        test_yaml = gemini_yaml_gen(
            f"Design a short coding task to verify the above answer. "
            "Return YAML with title, description, difficulty."
        )
        test_json = test_yaml or {}

    reasoning = (
        f"text={i_conf:.2f} "
        f"threshold={cfg.confidence_threshold}"
    )
    return EvaluationResponse(
        turn_id=req.turn_id,
        confidence_score=overall,
        decision=decision,
        reasoning=reasoning,
        suggested_test=test_json,
    )

@app.get("/healthz")
def health() -> Dict[str, str]:
    return {"status": "ok"}

'''
curl http://localhost:8000/evaluate `
  -Method POST `
  -Headers @{ 'Content-Type' = 'application/json' } `
  -Body (
    @{
      turn_id       = 'realTest1';
      text_response = 'complexity of bubble sort is O(n^5) in worst case';
      audio_url     = 'dummy.wav';                     # put a real .wav URL or local path if you have one
      image_urls    = @(
        'http://localhost:8000/static/face1.jpg',
        'http://localhost:8000/static/face2.jpg'
      )
    } | ConvertTo-Json -Depth 3
  )

'''