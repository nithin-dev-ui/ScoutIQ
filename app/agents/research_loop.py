class ResearchLoopAgent:
    """
    Controls iterative research rounds.

    The loop is intentionally limited so ScoutIQ does not
    consume excessive search API quota.
    """

    MAX_ROUNDS = 1
    MAX_FOLLOW_UP_QUERIES = 2

    def __init__(
        self,
        researcher,
        verifier,
        comparator,
        gap_analyzer
    ):
        self.researcher = researcher
        self.verifier = verifier
        self.comparator = comparator
        self.gap_analyzer = gap_analyzer

    def _build_follow_up_tasks(
        self,
        gap_analysis
    ):
        tasks = []

        for gap in gap_analysis.get("gaps", []):
            query = gap.get("query", "").strip()

            if not query:
                continue

            tasks.append({
                "type": "follow_up",
                "query": query
            })

            if len(tasks) >= self.MAX_FOLLOW_UP_QUERIES:
                break

        return tasks

    def run(
        self,
        question,
        initial_evidence,
        comparison=None
    ):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        evidence = list(initial_evidence or [])

        rounds = []

        for round_number in range(
            self.MAX_ROUNDS + 1
        ):
            verification = self.verifier.verify(
                evidence
            )

            verified_evidence = verification[
                "verified_evidence"
            ]

            current_comparison = comparison

            if current_comparison:
                topic_a = current_comparison.get(
                    "topic_a",
                    "Topic A"
                )
                topic_b = current_comparison.get(
                    "topic_b",
                    "Topic B"
                )

                current_comparison = (
                    self.comparator.compare(
                        verified_evidence,
                        topic_a=topic_a,
                        topic_b=topic_b
                    )
                )

            gap_analysis = self.gap_analyzer.analyze(
                question=question,
                evidence=verified_evidence,
                comparison=current_comparison
            )

            round_info = {
                "round": round_number,
                "evidence_count": len(evidence),
                "verified_count": len(
                    verified_evidence
                ),
                "gap_count": len(
                    gap_analysis.get("gaps", [])
                ),
                "follow_up_queries": []
            }

            # No follow-up after the final allowed round.
            if round_number >= self.MAX_ROUNDS:
                rounds.append(round_info)
                break

            # If no gaps exist, research is complete.
            if not gap_analysis.get(
                "has_gaps",
                False
            ):
                rounds.append(round_info)
                break

            follow_up_tasks = (
                self._build_follow_up_tasks(
                    gap_analysis
                )
            )

            round_info["follow_up_queries"] = [
                task["query"]
                for task in follow_up_tasks
            ]

            rounds.append(round_info)

            if not follow_up_tasks:
                break

            # Perform targeted follow-up research.
            new_evidence = self.researcher.research(
                follow_up_tasks
            )

            existing_links = {
                item.get("link", "")
                for item in evidence
            }

            for item in new_evidence:
                link = item.get("link", "")

                if link and link not in existing_links:
                    evidence.append(item)
                    existing_links.add(link)

        final_verification = self.verifier.verify(
            evidence
        )

        final_evidence = final_verification[
            "verified_evidence"
        ]

        final_comparison = comparison

        if final_comparison:
            topic_a = final_comparison.get(
                "topic_a",
                "Topic A"
            )
            topic_b = final_comparison.get(
                "topic_b",
                "Topic B"
            )

            final_comparison = (
                self.comparator.compare(
                    final_evidence,
                    topic_a=topic_a,
                    topic_b=topic_b
                )
            )

        final_gap_analysis = self.gap_analyzer.analyze(
            question=question,
            evidence=final_evidence,
            comparison=final_comparison
        )

        return {
            "evidence": evidence,
            "verification": final_verification,
            "comparison": final_comparison,
            "gap_analysis": final_gap_analysis,
            "rounds": rounds
        }