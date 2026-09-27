# ScoutIQ

### Evidence-First AI Research Intelligence Engine

ScoutIQ is an AI-powered research intelligence system that turns live web search into a transparent, evidence-grounded research pipeline.

Instead of asking an AI model to answer from static knowledge alone, ScoutIQ plans an investigation, retrieves live evidence through SerpApi, categorizes sources, identifies evidence gaps, performs limited follow-up research, and uses Gemini to produce a grounded research assessment.

---

## The Problem

AI-generated answers can be:

* Outdated
* Difficult to verify
* Missing supporting evidence
* Poor at comparing multiple information sources
* Unable to clearly identify what information is still missing

Traditional search engines provide links, but users still need to manually collect, verify, compare, and organize the information.

---

## The Solution

ScoutIQ combines:

* Live web search
* Research planning
* Evidence collection
* Source verification
* Comparison analysis
* Evidence-gap detection
* Targeted follow-up research
* Evidence-grounded AI reasoning
* Structured intelligence reports

The goal is to make research more **transparent, traceable, and evidence-driven**.

---

## Key Features

* Natural-language research questions
* Live multi-engine search through SerpApi
* Google Search integration
* Google News integration
* Google Scholar integration
* Google Jobs integration
* Source categorization
* Heuristic source-quality scoring
* Comparison research for multiple topics
* Evidence-gap detection
* Capped targeted follow-up research
* Gemini-powered evidence-grounded reasoning
* Transparent Research Trace
* Structured intelligence reports
* Source links and research limitations
* Offline automated testing for the research loop

---

## Research Pipeline

```text
User Question
      ↓
Research Planning
      ↓
Live SerpApi Search
      ↓
Evidence Collection
      ↓
Source Verification
      ↓
Comparison Analysis
      ↓
Evidence Gap Detection
      ↓
Targeted Follow-up Research
      ↓
Gemini Reasoning
      ↓
Intelligence Report
```

---

## Multi-Agent Architecture

ScoutIQ separates the research process into specialized components.

```text
                    ┌─────────────────────┐
                    │    User Question    │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Planner Agent      │
                    │ Research Planning   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Researcher Agent    │
                    │   SerpApi Search     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Verification Agent  │
                    │ Source Analysis     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Comparison Agent    │
                    │ Compare Evidence    │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Gap Analyzer Agent  │
                    │ Find Missing Areas  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Research Loop       │
                    │ Targeted Follow-up  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Gemini Reasoner     │
                    │ Evidence-grounded   │
                    │ AI Assessment       │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Intelligence Report │
                    └─────────────────────┘
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* python-dotenv

### AI

* Google Gemini
* `google-genai`

### Search

* SerpApi
* Google Search
* Google News
* Google Scholar
* Google Jobs

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* React Markdown

### Testing

* pytest
* Offline fake researcher for research-loop testing

---

## Project Structure

```text
ScoutIQ/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── verifier.py
│   │   ├── comparator.py
│   │   ├── gap_analyzer.py
│   │   ├── research_loop.py
│   │   ├── llm_reasoner.py
│   │   └── synthesizer.py
│   │
│   ├── services/
│   │   ├── serpapi_service.py
│   │   └── llm_service.py
│   │
│   ├── engine.py
│   └── api.py
│
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   ├── package.json
│   └── ...
│
├── tests/
│   └── test_research_loop.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Requirements

Before running ScoutIQ, install:

* Python 3.10+
* Node.js
* npm
* A SerpApi API key
* A Google Gemini API key

---

## Backend Setup

### 1. Clone the repository

```bash
git clone https://github.com/nithin-dev-ui/ScoutIQ.git
cd ScoutIQ
```

### 2. Create a Python virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
SERPAPI_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder values with your own API keys.

**Never commit your real API keys to GitHub.**

The `.gitignore` file excludes `.env` from version control.

---

## Start the Backend

From the project root:

```powershell
uvicorn app.api:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

## Frontend Setup

Open another terminal and move into the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

---

## Running an Investigation

1. Start the backend.
2. Start the frontend.
3. Open the frontend in your browser.
4. Enter a research question.
5. Start the investigation.
6. ScoutIQ plans the research.
7. SerpApi retrieves live evidence.
8. Evidence is verified and categorized.
9. Comparisons and evidence gaps are analyzed.
10. Targeted follow-up research is performed when required.
11. Gemini generates an evidence-grounded assessment.
12. ScoutIQ displays the structured intelligence report.

---

## Example Research Question

```text
Should students learn Python or JavaScript first for AI software careers in 2026?
```

ScoutIQ can use multiple search strategies for the investigation, including general web results, recent news, expert/research sources, and comparison-specific searches.

---

## Research Trace

ScoutIQ exposes a Research Trace showing how the investigation was assembled.

A trace can include:

```text
Query Type
Engine
Evidence Count
```

This helps users understand which search paths contributed to the final research result.

---

## Evidence Verification

ScoutIQ categorizes retrieved sources and applies heuristic quality scoring.

The system can distinguish between different source types and preserve source metadata such as:

* Source title
* URL
* Domain
* Source type
* Search engine
* Query type
* Quality score

The goal is not to treat every search result as equally reliable.

---

## Evidence Gap Detection

ScoutIQ analyzes the collected evidence for areas that may require additional research.

When appropriate, the research loop can generate a limited number of targeted follow-up queries.

This prevents the system from endlessly searching while still allowing it to investigate important missing evidence.

---

## AI Reasoning

Gemini is used after the evidence collection and analysis stages.

ScoutIQ provides the collected evidence to the reasoning layer so that the generated assessment is grounded in the research gathered during the investigation.

The system also preserves limitations and source information instead of presenting the AI output as unsupported fact.

---

## Testing

ScoutIQ includes an offline test for the research loop.

The test uses a `FakeResearcher`, so it does **not** call SerpApi or consume search API quota.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Expected result:

```text
1 passed
```

The test verifies the research loop's ability to:

* Process initial evidence
* Perform follow-up research
* Expand the evidence set
* Run verification
* Run gap analysis

---

## Production Build

To verify the Next.js frontend production build:

```powershell
cd frontend
npm run build
```

A successful build confirms that the frontend compiles and passes the TypeScript/build checks.

---

## API Endpoint

ScoutIQ exposes the main research endpoint:

```text
POST /research
```

Example request:

```json
{
  "question": "Should students learn Python or JavaScript first for AI software careers in 2026?"
}
```

The endpoint returns structured research information including evidence counts, research rounds, gap analysis, AI reasoning status, and the generated report.

---

## API Health Check

```text
GET /health
```

This endpoint can be used to verify that the backend is running.

---

## Design Philosophy

ScoutIQ follows an **evidence-first** approach:

```text
Search → Verify → Compare → Find Gaps → Research → Reason → Report
```

Rather than hiding the research process behind a single AI response, ScoutIQ exposes the stages that contribute to the final result.

---

## Limitations

ScoutIQ currently depends on external services for live search and AI reasoning.

Important limitations include:

* SerpApi usage is subject to the user's API plan and quota.
* Gemini usage is subject to the selected model's availability and API limits.
* Source-quality scoring is heuristic and should not be treated as an absolute measure of source credibility.
* Search results can change over time.
* AI reasoning should be checked against the underlying evidence and source links.
* The current automated test suite covers the research loop rather than every component of the application.

---

## Security

API keys are stored in environment variables and should never be committed to the repository.

For local development:

```text
.env
```

is intentionally excluded through `.gitignore`.

---

## Project Status

ScoutIQ currently includes:

* Live SerpApi research
* Multi-engine search routing
* Research planning
* Source verification
* Comparison analysis
* Evidence-gap detection
* Targeted follow-up research
* Gemini reasoning
* Structured intelligence reports
* Research Trace
* Next.js frontend
* FastAPI backend
* Automated research-loop testing

---

## License

This project is currently provided as a hackathon project.
