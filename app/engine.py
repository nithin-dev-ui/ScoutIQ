from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent
from app.agents.verifier import VerificationAgent
from app.agents.comparator import ComparisonAgent
from app.agents.synthesizer import SynthesisAgent
from app.agents.llm_reasoner import LLMReasonerAgent
from app.agents.gap_analyzer import GapAnalyzerAgent
from app.agents.research_loop import ResearchLoopAgent
from app.services.llm_service import LLMService


class ScoutIQEngine:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.verifier = VerificationAgent()
        self.comparator = ComparisonAgent()
        self.synthesizer = SynthesisAgent()

        self.llm_reasoner = LLMReasonerAgent()
        self.llm_service = LLMService()
        self.gap_analyzer = GapAnalyzerAgent()

        self.research_loop = ResearchLoopAgent(
            researcher=self.researcher,
            verifier=self.verifier,
            comparator=self.comparator,
            gap_analyzer=self.gap_analyzer
        )

    def investigate(self, question):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        question = question.strip()

        # 1. Planner decides what research is required.
        plan = self.planner.create_plan(question)

        # 2. Execute initial research using SerpApi.
        initial_evidence = self.researcher.research(
            plan["queries"]
        )

        # 3. Build the initial comparison if required.
        initial_verification = self.verifier.verify(
            initial_evidence
        )

        initial_verified_evidence = (
            initial_verification["verified_evidence"]
        )

        comparison = None

        if plan.get("comparison", False):
            topics = plan.get(
                "comparison_topics",
                []
            )

            if len(topics) == 2:
                comparison = self.comparator.compare(
                    initial_verified_evidence,
                    topic_a=topics[0],
                    topic_b=topics[1]
                )

        # 4. Run iterative research.
        research_result = self.research_loop.run(
            question=question,
            initial_evidence=initial_evidence,
            comparison=comparison
        )

        evidence = research_result["evidence"]
        verification = research_result["verification"]

        verified_evidence = verification[
            "verified_evidence"
        ]

        comparison = research_result["comparison"]
        gap_analysis = research_result["gap_analysis"]

        # 5. Build grounded LLM reasoning prompt.
        llm_prompt = None
        llm_reasoning = None
        llm_status = "not_configured"

        if verified_evidence:
            llm_prompt = self.llm_reasoner.build_prompt(
                question=question,
                verified_evidence=verified_evidence,
                comparison=comparison
            )

            # 6. Use Gemini when configured.
            if self.llm_service.is_available():
                llm_reasoning = self.llm_service.generate(
                    llm_prompt
                )
                llm_status = "generated"
            else:
                llm_status = "not_configured"

        # 7. Generate the final structured report.
        report = self.synthesizer.create_report(
            question=question,
            verified_evidence=verified_evidence,
            comparison=comparison,
            source_stats=verification["source_stats"],
            issues=verification["issues"]
        )

        # 8. Attach Gemini reasoning to the report.
        # This allows the frontend to display it.
        report["ai_reasoning"] = llm_reasoning
        report["ai_reasoning_status"] = llm_status

        return {
            "question": question,
            "plan": plan,
            "initial_evidence_count": len(
                initial_evidence
            ),
            "evidence_count": len(evidence),
            "verification": verification,
            "comparison": comparison,
            "gap_analysis": gap_analysis,
            "research_loop": {
                "rounds": research_result["rounds"]
            },
            "llm": {
                "status": llm_status,
                "reasoning": llm_reasoning,
                "prompt": llm_prompt
            },
            "report": report
        }

    def build_report_from_evidence(
        self,
        question,
        evidence
    ):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        question = question.strip()

        # 1. Verify supplied evidence without searching.
        verification = self.verifier.verify(evidence)

        verified_evidence = verification[
            "verified_evidence"
        ]

        # 2. Detect comparison.
        plan = self.planner.create_plan(question)

        comparison = None

        if plan.get("comparison", False):
            topics = plan.get(
                "comparison_topics",
                []
            )

            if len(topics) == 2:
                comparison = self.comparator.compare(
                    verified_evidence,
                    topic_a=topics[0],
                    topic_b=topics[1]
                )

        # 3. Analyze gaps without searching.
        gap_analysis = self.gap_analyzer.analyze(
            question=question,
            evidence=verified_evidence,
            comparison=comparison
        )

        # 4. Build grounded LLM prompt.
        llm_prompt = None

        if verified_evidence:
            llm_prompt = self.llm_reasoner.build_prompt(
                question=question,
                verified_evidence=verified_evidence,
                comparison=comparison
            )

        # 5. Generate structured report.
        report = self.synthesizer.create_report(
            question=question,
            verified_evidence=verified_evidence,
            comparison=comparison,
            source_stats=verification["source_stats"],
            issues=verification["issues"]
        )

        # This method does not call Gemini.
        # Therefore, no undefined LLM variables are used here.
        report["ai_reasoning"] = None
        report["ai_reasoning_status"] = "not_called"

        return {
            "question": question,
            "verification": verification,
            "comparison": comparison,
            "gap_analysis": gap_analysis,
            "llm": {
                "status": "not_called",
                "reasoning": None,
                "prompt": llm_prompt
            },
            "report": report
        }