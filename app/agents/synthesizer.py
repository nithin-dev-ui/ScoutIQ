class SynthesisAgent:
    def _rank_evidence(self, verified_evidence):
        return sorted(
            verified_evidence,
            key=lambda item: (
                item.get("quality_score", 0),
                item.get("completeness", 0),
                -item.get("position", 999)
            ),
            reverse=True
        )

    def _build_finding(self, item):
        snippet = (item.get("snippet") or "").strip()
        title = (item.get("title") or "").strip()
        source_type = (
            item.get("source_type") or "Other"
        ).strip()
        domain = (item.get("domain") or "").strip()

        if snippet:
            return snippet

        if title:
            return (
                f"The source titled '{title}' "
                f"provides relevant evidence for this "
                f"investigation."
            )

        if domain:
            return (
                f"Relevant evidence was identified from "
                f"{domain} ({source_type})."
            )

        return (
            "Relevant evidence was identified, but the "
            "source did not provide a usable text summary."
        )

    def create_report(
        self,
        question,
        verified_evidence,
        comparison=None,
        source_stats=None,
        issues=None
    ):
        if not verified_evidence:
            return {
                "question": question,
                "summary": "No usable evidence was found.",
                "key_findings": [],
                "comparison": comparison or {},
                "source_analysis": source_stats or {},
                "limitations": issues or [],
                "sources": [],
                "research_trace": []
            }

        ranked_evidence = self._rank_evidence(
            verified_evidence
        )

        key_findings = []

        for item in ranked_evidence[:5]:
            key_findings.append({
                "finding": self._build_finding(item),
                "source": item.get("title", ""),
                "domain": item.get("domain", ""),
                "source_type": item.get(
                    "source_type",
                    "Other"
                ),
                "query_type": item.get(
                    "query_type",
                    "web"
                ),
                "engine": item.get(
                    "engine",
                    "unknown"
                ),
                "quality_score": item.get(
                    "quality_score",
                    0
                ),
                "link": item.get("link", "")
            })

        source_count = 0

        if source_stats:
            source_count = source_stats.get(
                "unique_sources",
                0
            )

        average_quality_score = 0

        if source_stats:
            average_quality_score = source_stats.get(
                "average_quality_score",
                0
            )

        report_sources = []
        seen_links = set()

        for item in ranked_evidence:
            link = item.get("link", "")

            if link and link not in seen_links:
                seen_links.add(link)

                report_sources.append({
                    "title": item.get(
                        "title",
                        ""
                    ),
                    "domain": item.get(
                        "domain",
                        ""
                    ),
                    "source_type": item.get(
                        "source_type",
                        "Other"
                    ),
                    "quality_score": item.get(
                        "quality_score",
                        0
                    ),
                    "query_type": item.get(
                        "query_type",
                        "web"
                    ),
                    "engine": item.get(
                        "engine",
                        "unknown"
                    ),
                    "link": link
                })

            if len(report_sources) >= 10:
                break

        # Build a compact research trace from the actual
        # evidence collected by ScoutIQ.
        trace_map = {}

        for item in verified_evidence:
            query_type = item.get(
                "query_type",
                "web"
            )

            engine = item.get(
                "engine",
                "unknown"
            )

            key = (
                f"{query_type}|{engine}"
            )

            if key not in trace_map:
                trace_map[key] = {
                    "query_type": query_type,
                    "engine": engine,
                    "evidence_count": 0
                }

            trace_map[key]["evidence_count"] += 1

        research_trace = list(
            trace_map.values()
        )

        summary = (
            f"ScoutIQ analyzed "
            f"{len(verified_evidence)} "
            f"evidence items from "
            f"{source_count} "
            f"unique sources. The report "
            f"prioritizes evidence using a "
            f"source-quality heuristic with "
            f"an average score of "
            f"{average_quality_score}."
        )

        return {
            "question": question,
            "summary": summary,
            "key_findings": key_findings,
            "comparison": comparison or {},
            "source_analysis": source_stats or {},
            "limitations": issues or [],
            "sources": report_sources,
            "research_trace": research_trace
        }