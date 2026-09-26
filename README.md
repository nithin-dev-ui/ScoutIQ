# ScoutIQ

### Evidence-First AI Research Intelligence Engine

ScoutIQ is an AI-powered research intelligence system that turns live web search into a transparent, evidence-grounded research pipeline.

Instead of asking an AI model to answer from static knowledge alone, ScoutIQ plans an investigation, retrieves live evidence through SerpApi, categorizes sources, identifies evidence gaps, performs limited follow-up research, and uses Gemini to produce a grounded research assessment.

## The Problem

AI-generated answers can be outdated, difficult to verify, or disconnected from the evidence supporting them. Traditional search engines provide links but leave users to manually organize and compare the results.

## The Solution

ScoutIQ combines live search, evidence organization, source analysis, comparison, gap detection, and AI reasoning in one research workflow.

## Example Research Question

> Should students learn Python or JavaScript first for AI software careers in 2026?

## Key Features

- Research planning from natural-language questions
- Live multi-engine search through SerpApi
- Google Search, Google News, Google Scholar, and Google Jobs
- Source categorization and heuristic quality scoring
- Comparison research for multiple topics
- Evidence-gap detection
- Capped, targeted follow-up research
- Evidence-grounded Gemini reasoning
- Transparent Research Trace
- Structured intelligence reports with source links and limitations

## Research Pipeline

```text
User Question
    -> Research Planning
    -> Live SerpApi Search
    -> Evidence Collection
    -> Source Verification
    -> Comparison Analysis
    -> Evidence Gap Detection
    -> Targeted Follow-up Research
    -> Gemini Reasoning
    -> Intelligence Report