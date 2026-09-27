from app.agents.research_loop import ResearchLoopAgent
from app.agents.verifier import VerificationAgent
from app.agents.comparator import ComparisonAgent
from app.agents.gap_analyzer import GapAnalyzerAgent


class FakeResearcher:
    """
    Fake researcher used only for offline testing.

    This does NOT call SerpApi and does NOT consume API quota.
    """

    def research(self, queries):
        results = []

        for task in queries:
            query = task.get("query", "")

            results.append({
                "title": "JavaScript Developer Research",
                "link": "https://developer.mozilla.org/",
                "snippet": (
                    "JavaScript is widely used for web development "
                    "and AI-powered web applications."
                ),
                "source": "developer.mozilla.org",
                "query": query,
                "query_type": task.get(
                    "type",
                    "follow_up"
                ),
                "engine": "google",
                "position": 1
            })

        return results


def test_research_loop():
    researcher = FakeResearcher()
    verifier = VerificationAgent()
    comparator = ComparisonAgent()
    gap_analyzer = GapAnalyzerAgent()

    loop = ResearchLoopAgent(
        researcher=researcher,
        verifier=verifier,
        comparator=comparator,
        gap_analyzer=gap_analyzer
    )

    question = (
        "Should students learn Python or JavaScript first "
        "for AI software careers in 2026?"
    )

    initial_evidence = [
        {
            "title": "Python Documentation",
            "link": "https://python.org",
            "snippet": (
                "Python is widely used in software development."
            ),
            "source": "python.org",
            "query": "Python AI careers",
            "query_type": "comparison_a",
            "engine": "google",
            "position": 1
        },
        {
            "title": "AI Research Paper",
            "link": "https://arxiv.org/abs/1234.5678",
            "snippet": (
                "Artificial intelligence research uses "
                "multiple programming languages."
            ),
            "source": "arxiv.org",
            "query": "AI programming languages",
            "query_type": "expert",
            "engine": "google_scholar",
            "position": 1
        }
    ]

    result = loop.run(
        question=question,
        initial_evidence=initial_evidence,
        comparison={
            "topic_a": "Python",
            "topic_b": "JavaScript"
        }
    )

    assert len(result["evidence"]) >= len(initial_evidence)
    assert len(result["rounds"]) >= 1
    assert "verification" in result
    assert "gap_analysis" in result
    assert len(result["verification"]["verified_evidence"]) >= 1
    assert "gaps" in result["gap_analysis"]