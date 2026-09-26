class ComparisonAgent:
    def compare(self, evidence, topic_a="Python", topic_b="JavaScript"):
        if not evidence:
            return {
                "topic_a": topic_a,
                "topic_b": topic_b,
                "a_evidence": [],
                "b_evidence": [],
                "shared_evidence": [],
                "stats": {
                    "topic_a_results": 0,
                    "topic_b_results": 0,
                    "shared_results": 0
                }
            }

        a_evidence = []
        b_evidence = []
        shared_evidence = []

        topic_a_terms = [
            topic_a.lower(),
            f"{topic_a.lower()} programming",
            f"{topic_a.lower()} developer",
            f"{topic_a.lower()} development"
        ]

        topic_b_terms = [
            topic_b.lower(),
            f"{topic_b.lower()} programming",
            f"{topic_b.lower()} developer",
            f"{topic_b.lower()} development"
        ]

        for item in evidence:
            title = item.get("title", "").lower()
            snippet = item.get("snippet", "").lower()

            text = f"{title} {snippet}"

            has_a = any(term in text for term in topic_a_terms)
            has_b = any(term in text for term in topic_b_terms)

            if has_a and has_b:
                shared_evidence.append(item)

            elif has_a:
                a_evidence.append(item)

            elif has_b:
                b_evidence.append(item)

        return {
            "topic_a": topic_a,
            "topic_b": topic_b,
            "a_evidence": a_evidence,
            "b_evidence": b_evidence,
            "shared_evidence": shared_evidence,
            "stats": {
                "topic_a_results": len(a_evidence),
                "topic_b_results": len(b_evidence),
                "shared_results": len(shared_evidence)
            }
        }