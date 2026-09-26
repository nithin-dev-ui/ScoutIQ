class GapAnalyzerAgent:
    """
    Analyzes collected evidence and identifies missing
    research areas that may require follow-up searches.

    Follow-up queries are intentionally concise and
    targeted at the detected research gap.
    """

    def _comparison_context(
        self,
        question,
        comparison
    ):
        if not comparison:
            return question

        topic_a = comparison.get(
            "topic_a",
            "Topic A"
        )

        topic_b = comparison.get(
            "topic_b",
            "Topic B"
        )

        return f"{topic_a} {topic_b}"

    def analyze(
        self,
        question,
        evidence,
        comparison=None
    ):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        question = question.strip()

        context = self._comparison_context(
            question,
            comparison
        )

        if not evidence:
            return {
                "has_gaps": True,
                "gaps": [
                    {
                        "type": "general",
                        "description": (
                            "No evidence was collected."
                        ),
                        "query": (
                            f"{context} latest evidence 2026"
                        )
                    }
                ]
            }

        gaps = []

        # -------------------------------------------------
        # 1. Check evidence volume
        # -------------------------------------------------
        complete_evidence = [
            item
            for item in evidence
            if item.get("title")
            and item.get("snippet")
            and item.get("link")
        ]

        if len(complete_evidence) < 3:
            gaps.append({
                "type": "evidence_volume",
                "description": (
                    "Too little complete evidence is "
                    "available for a reliable synthesis."
                ),
                "query": (
                    f"{context} reliable evidence 2026"
                )
            })

        # -------------------------------------------------
        # 2. Check comparison balance
        # -------------------------------------------------
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

            count_a = stats.get(
                "topic_a_results",
                0
            )

            count_b = stats.get(
                "topic_b_results",
                0
            )

            if count_a == 0:
                gaps.append({
                    "type": "comparison_balance",
                    "description": (
                        f"No evidence specifically "
                        f"supports {topic_a}."
                    ),
                    "query": (
                        f"{topic_a} AI software "
                        "development careers 2026"
                    )
                })

            if count_b == 0:
                gaps.append({
                    "type": "comparison_balance",
                    "description": (
                        f"No evidence specifically "
                        f"supports {topic_b}."
                    ),
                    "query": (
                        f"{topic_b} AI software "
                        "development careers 2026"
                    )
                })

            # Detect heavily unbalanced comparisons.
            if count_a > 0 and count_b > 0:
                larger = max(
                    count_a,
                    count_b
                )

                smaller = min(
                    count_a,
                    count_b
                )

                if smaller * 3 < larger:
                    weaker_topic = (
                        topic_a
                        if count_a < count_b
                        else topic_b
                    )

                    gaps.append({
                        "type": "comparison_balance",
                        "description": (
                            "The comparison has substantially "
                            "more evidence for one side than "
                            "the other. More evidence is needed "
                            f"for {weaker_topic}."
                        ),
                        "query": (
                            f"{weaker_topic} AI software "
                            "development careers 2026"
                        )
                    })

        # -------------------------------------------------
        # 3. Check source diversity
        # -------------------------------------------------
        source_types = {
            item.get(
                "source_type",
                "Other"
            )
            for item in evidence
        }

        if len(source_types) == 1:
            only_type = next(
                iter(source_types)
            )

            gaps.append({
                "type": "source_diversity",
                "description": (
                    "Evidence comes from only one "
                    f"source category: {only_type}."
                ),
                "query": (
                    f"{context} government "
                    "research expert analysis 2026"
                )
            })

        # -------------------------------------------------
        # 4. Check quantitative evidence
        # -------------------------------------------------
        data_keywords = [
            "percent",
            "%",
            "statistics",
            "survey",
            "salary",
            "growth",
            "market",
            "employment",
            "jobs",
            "demand"
        ]

        evidence_text = " ".join(
            (
                item.get("title", "")
                + " "
                + item.get("snippet", "")
            ).lower()
            for item in evidence
        )

        has_data = any(
            keyword in evidence_text
            for keyword in data_keywords
        )

        if not has_data:
            gaps.append({
                "type": "data",
                "description": (
                    "The collected evidence does not "
                    "contain clear quantitative or "
                    "market data."
                ),
                "query": (
                    f"{context} statistics salary "
                    "jobs demand 2026"
                )
            })

        # -------------------------------------------------
        # 5. Remove duplicate queries
        # -------------------------------------------------
        unique_gaps = []
        seen_queries = set()

        for gap in gaps:
            query = gap.get(
                "query",
                ""
            ).strip()

            if not query:
                continue

            normalized_query = query.lower()

            if normalized_query in seen_queries:
                continue

            seen_queries.add(
                normalized_query
            )

            unique_gaps.append(gap)

        return {
            "has_gaps": len(unique_gaps) > 0,
            "gaps": unique_gaps
        }