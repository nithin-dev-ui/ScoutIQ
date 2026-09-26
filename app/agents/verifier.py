from urllib.parse import urlparse


class VerificationAgent:
    SOURCE_SCORES = {
        "Government / Official": 5,
        "Academic / Educational": 5,
        "Academic / Research": 5,
        "News": 4,
        "Community": 3,
        "Other": 2
    }

    def classify_source(self, domain):
        domain = domain.lower()

        if domain.endswith(".gov") or ".gov." in domain:
            return "Government / Official"

        if domain.endswith(".edu") or ".edu." in domain:
            return "Academic / Educational"

        academic_domains = [
            "arxiv.org",
            "nature.com",
            "sciencedirect.com",
            "springer.com",
            "ieee.org",
            "acm.org"
        ]

        if any(
            domain == item or domain.endswith("." + item)
            for item in academic_domains
        ):
            return "Academic / Research"

        news_domains = [
            "reuters.com",
            "bbc.com",
            "cnn.com",
            "theguardian.com",
            "nytimes.com",
            "economictimes.indiatimes.com",
            "timesofindia.indiatimes.com"
        ]

        if any(
            domain == item or domain.endswith("." + item)
            for item in news_domains
        ):
            return "News"

        community_domains = [
            "reddit.com",
            "quora.com",
            "stackoverflow.com"
        ]

        if any(
            domain == item or domain.endswith("." + item)
            for item in community_domains
        ):
            return "Community"

        return "Other"

    def calculate_quality_score(
        self,
        source_type,
        completeness,
        position
    ):
        score = self.SOURCE_SCORES.get(source_type, 2)

        # Complete results receive a small reliability bonus.
        if completeness == 3:
            score += 2

        # Earlier search positions receive a small relevance bonus.
        if position and position <= 3:
            score += 1
        elif position and position <= 10:
            score += 0.5

        return min(round(score, 1), 8)

    def verify(self, evidence):
        if not evidence:
            return {
                "status": "insufficient",
                "verified_evidence": [],
                "issues": ["No evidence was found."],
                "source_stats": {
                    "total_results": 0,
                    "unique_sources": 0,
                    "complete_results": 0,
                    "source_types": {},
                    "average_quality_score": 0
                }
            }

        verified_evidence = []
        seen_links = set()
        seen_domains = set()
        issues = []
        source_types = []

        for item in evidence:
            title = item.get("title", "").strip()
            link = item.get("link", "").strip()
            snippet = item.get("snippet", "").strip()
            query_type = item.get("query_type", "web")
            position = item.get("position", 0)

            if not title or not link:
                issues.append(
                    "A search result was missing a title or link."
                )
                continue

            if link in seen_links:
                continue

            seen_links.add(link)

            parsed_url = urlparse(link)
            domain = parsed_url.netloc.lower()

            if domain.startswith("www."):
                domain = domain[4:]

            if not domain:
                issues.append(f"Invalid source URL: {link}")
                continue

            seen_domains.add(domain)

            source_type = self.classify_source(domain)

            completeness = 0

            if title:
                completeness += 1

            if link:
                completeness += 1

            if snippet:
                completeness += 1

            quality_score = self.calculate_quality_score(
                source_type=source_type,
                completeness=completeness,
                position=position
            )

            source_types.append(source_type)

            verified_evidence.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "source": item.get("source", ""),
                "query": item.get("query", ""),
                "query_type": query_type,
                "engine": item.get("engine", "unknown"),
                "domain": domain,
                "source_type": source_type,
                "completeness": completeness,
                "quality_score": quality_score,
                "validated": completeness == 3
            })

        complete_results = sum(
            1
            for item in verified_evidence
            if item["validated"]
        )

        unique_sources = len(seen_domains)

        source_type_counts = {}

        for source_type in source_types:
            source_type_counts[source_type] = (
                source_type_counts.get(source_type, 0) + 1
            )

        if verified_evidence:
            average_quality_score = round(
                sum(
                    item["quality_score"]
                    for item in verified_evidence
                ) / len(verified_evidence),
                2
            )

            status = "validated"
        else:
            average_quality_score = 0
            status = "insufficient"

        return {
            "status": status,
            "verified_evidence": verified_evidence,
            "issues": issues,
            "source_stats": {
                "total_results": len(evidence),
                "unique_sources": unique_sources,
                "complete_results": complete_results,
                "source_types": source_type_counts,
                "average_quality_score": average_quality_score
            }
        }