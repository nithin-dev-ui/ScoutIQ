from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.engine import ScoutIQEngine


app = FastAPI(
    title="ScoutIQ API",
    description=(
        "AI-powered research and intelligence API "
        "using SerpApi and Gemini."
    ),
    version="1.0.0"
)


# Allow the Next.js frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    question: str
    evidence_count: int
    research_rounds: int
    gap_count: int
    llm_status: str
    report: dict


@app.get("/")
def root():
    return {
        "name": "ScoutIQ",
        "status": "online",
        "message": "ScoutIQ research API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        engine = ScoutIQEngine()

        result = engine.investigate(
            question
        )

        return ResearchResponse(
            question=result["question"],
            evidence_count=result["evidence_count"],
            research_rounds=len(
                result["research_loop"]["rounds"]
            ),
            gap_count=len(
                result["gap_analysis"]["gaps"]
            ),
            llm_status=result["llm"]["status"],
            report=result["report"]
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )