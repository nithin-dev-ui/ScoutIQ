class LLMReasonerAgent:
    """
    Builds grounded reasoning prompts for the LLM.

    The agent does not perform web searches itself.
    It reasons over evidence collected by SerpApi.
    """

    def build_prompt(
        self,
        question,
        verified_evidence,
        comparison=None
    ):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        if not verified_evidence:
            raise ValueError(
                "No verified evidence was provided"
            )

        evidence_lines = []

        for index, item in enumerate(
            verified_evidence,
            start=1
        ):
            evidence_lines.append(
                f"""
Evidence {index}:
Title: {item.get("title", "")}
Domain: {item.get("domain", "")}
Source type: {item.get("source_type", "Other")}
Quality heuristic: {item.get("quality_score", 0)}
Search type: {item.get("query_type", "web")}
Snippet: {item.get("snippet", "")}
URL: {item.get("link", "")}
""".strip()
            )

        evidence_text = "\n\n".join(evidence_lines)

        comparison_text = "No comparison was requested."

        if comparison:
            topic_a = comparison.get(
                "topic_a",
                "Topic A"
            )
            topic_b = comparison.get(
                "topic_b",
                "Topic B"
            )

            stats = comparison.get(
                "stats",
                {}
            )

            comparison_text = f"""
Comparison requested:
Topic A: {topic_a}
Topic B: {topic_b}

Evidence counts:
{topic_a}: {stats.get("topic_a_results", 0)}
{topic_b}: {stats.get("topic_b_results", 0)}
Shared evidence: {stats.get("shared_results", 0)}
""".strip()

        prompt = f"""
You are the reasoning agent inside ScoutIQ,
an AI research and intelligence system.

Your job is to analyze evidence retrieved from
search engines and produce an evidence-grounded
research assessment.

Research question:
{question}

{comparison_text}

Retrieved evidence:
{evidence_text}

Instructions:

1. Use only the supplied evidence.
2. Do not invent facts, statistics, sources,
   URLs, quotations, or citations.
3. Distinguish directly supported findings from
   reasonable interpretations.
4. If the evidence is insufficient, explicitly
   say that it is insufficient.
5. Do not treat the quality heuristic as proof
   that a source is factually correct.
6. For comparisons, describe evidence for both
   sides before drawing any synthesis.
7. Identify important limitations, conflicts,
   uncertainty, or evidence-quality weaknesses.
8. Do not describe the evidence as "unanimous"
   unless the supplied evidence genuinely supports
   that characterization.
9. Prefer calibrated language such as:
   "the retrieved evidence broadly supports",
   "the evidence is consistent with",
   "several sources indicate", or
   "the available evidence suggests".
10. Keep the reasoning concise and useful.

Return the following structure:

SUMMARY:
A concise evidence-grounded answer.

KEY FINDINGS:
- Finding 1
- Finding 2
- Finding 3

COMPARISON:
Describe the evidence for each side if applicable.

LIMITATIONS:
- Limitation 1
- Limitation 2

CONFIDENCE:
Low, Medium, or High, with one short reason.
""".strip()

        return prompt