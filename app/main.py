from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Literal

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, EmailStr, Field

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="AI Football Platform API", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Environment(loader=FileSystemLoader(ROOT / "templates"))
LEADS: list[dict] = []
JOBS: dict[str, dict] = {}

class Lead(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    role: Literal["player_parent", "coach", "academy_club", "scout_agent", "federation_league"]
    intent: Literal["join", "demo"] = "join"

class Analysis(BaseModel):
    video_url: str = "demo://sample"
    player_id: str | None = None
    drill_type: str = "ball_mastery"
    consent_confirmed: bool = True

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.get_template("index.html").render()

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": "aifp-api", "time": datetime.now(timezone.utc)}

@app.get("/api/v1/platform")
def platform():
    return {
        "entry_point": "SSOT",
        "roles": ["player_parent", "coach", "academy_club", "scout_agent", "federation_league"],
        "layers": ["player_development", "coach_assistant", "skill_passport", "academy_operations", "talent_intelligence"],
        "trust_controls": ["identity", "credential", "consent", "evidence_provenance"],
    }

@app.post("/api/v1/leads", status_code=201)
def create_lead(payload: Lead):
    record = {"id": str(uuid4()), **payload.model_dump(), "created_at": datetime.now(timezone.utc).isoformat()}
    LEADS.append(record)
    return record

def finish_analysis(job_id: str):
    JOBS[job_id].update(status="complete", scores={"ball_control": 86, "body_balance": 81, "decision_speed": 78}, next_action="Repeat the drill at match speed and scan before the first touch.")

@app.post("/api/v1/analyses", status_code=202)
def create_analysis(payload: Analysis, tasks: BackgroundTasks):
    if not payload.consent_confirmed:
        raise HTTPException(422, "Player or guardian consent is required.")
    job_id = str(uuid4())
    JOBS[job_id] = {"id": job_id, "status": "processing", **payload.model_dump()}
    tasks.add_task(finish_analysis, job_id)
    return JOBS[job_id]

@app.get("/api/v1/analyses/{job_id}")
def get_analysis(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(404, "Analysis not found")
    return JOBS[job_id]

@app.get("/api/v1/players/{player_id}/passport")
def passport(player_id: str):
    return {"player_id": player_id, "verification": "verified", "scores": {"first_touch": 88, "passing": 84, "dribbling": 79, "decision_speed": 82}, "evidence_quality": 0.91, "sharing": "consent_required"}
