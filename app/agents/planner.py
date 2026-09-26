import re


class PlannerAgent:
    def create_plan(self, question):
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty")

        comparison = self.detect_comparison(question)

        queries = [
            {
                "type": "web",
                "query": question
            },
            {
                "type": "latest",
                "query": f"{question} latest information 2026"
            },
            {
                "type": "data",
                "query": f"{question} statistics data 2026"
            },
            {
                "type": "expert",
                "query": f"{question} expert analysis research"
            }
        ]

        # Add dedicated searches when a comparison is detected.
        if comparison:
            topics = self.extract_comparison_topics(question)

            if topics:
                topic_a, topic_b = topics

                queries.extend([
                    {
                        "type": "comparison_a",
                        "query": f"{topic_a} AI software career 2026"
                    },
                    {
                        "type": "comparison_b",
                        "query": f"{topic_b} AI software career 2026"
                    },
                    {
                        "type": "comparison",
                        "query": f"{topic_a} vs {topic_b} AI development 2026"
                    }
                ])

        return {
            "question": question,
            "queries": queries,
            "comparison": comparison,
            "comparison_topics": (
                self.extract_comparison_topics(question)
                if comparison
                else []
            )
        }

    def detect_comparison(self, question):
        text = question.lower()

        comparison_words = [
            " vs ",
            " versus ",
            " or ",
            "compare ",
            "comparison",
            "which is better",
            "which should",
            "difference between"
        ]

        return any(word in text for word in comparison_words)

    def extract_comparison_topics(self, question):
        text = question.strip()

        # Pattern 1: "A vs B"
        match = re.search(
            r"\b(.+?)\s+vs\.?\s+(.+?)(?:\s+(?:for|in|on|to)\s+|$)",
            text,
            re.IGNORECASE
        )

        if match:
            return [
                match.group(1).strip(),
                match.group(2).strip()
            ]

        # Pattern 2: "A versus B"
        match = re.search(
            r"\b(.+?)\s+versus\s+(.+?)(?:\s+(?:for|in|on|to)\s+|$)",
            text,
            re.IGNORECASE
        )

        if match:
            return [
                match.group(1).strip(),
                match.group(2).strip()
            ]

        # Pattern 3: "learn A or B"
        match = re.search(
            r"\b(?:learn|choose|use|pick)\s+(.+?)\s+or\s+(.+?)(?:\s+(?:first|for|in|on|to)\b|[?.!]|$)",
            text,
            re.IGNORECASE
        )

        if match:
            return [
                match.group(1).strip(),
                match.group(2).strip()
            ]

        # Pattern 4: "A or B"
        match = re.search(
            r"\b([A-Z][A-Za-z0-9+#.-]{1,30})\s+or\s+([A-Z][A-Za-z0-9+#.-]{1,30})\b",
            text
        )

        if match:
            return [
                match.group(1).strip(),
                match.group(2).strip()
            ]

        return []