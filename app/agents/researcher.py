from app.services.serpapi_service import SerpApiService


class ResearchAgent:
    MAX_RESULTS_PER_TASK = 10

    def __init__(self):
        self.search_service = SerpApiService()

    def _search_by_type(self, query, query_type):
        if query_type == "latest":
            return self.search_service.google_news_search(query), "google_news"

        if query_type == "expert":
            return self.search_service.google_scholar_search(query), "google_scholar"

        if query_type == "jobs":
            return self.search_service.google_jobs_search(query), "google_jobs"

        return self.search_service.google_search(query), "google"

    def _extract_results(self, results, query_type):
        if query_type == "latest":
            return results.get("news_results", [])

        if query_type == "jobs":
            return results.get("jobs_results", [])

        return results.get("organic_results", [])

    def _normalize_source(self, result):
        source = result.get("displayed_link", "")

        if not source:
            source = result.get("source", "")

        if isinstance(source, dict):
            source = source.get("name", "")

        return str(source)

    def research(self, queries):
        if not queries:
            raise ValueError("No research queries provided")

        evidence = []
        seen_links = set()

        for task in queries:
            query_type = task.get("type", "web")
            query = task.get("query", "").strip()

            if not query:
                continue

            results, engine = self._search_by_type(
                query,
                query_type
            )

            search_results = self._extract_results(
                results,
                query_type
            )

            task_count = 0

            for result in search_results:
                if task_count >= self.MAX_RESULTS_PER_TASK:
                    break

                title = result.get("title", "").strip()
                link = result.get("link", "").strip()
                snippet = result.get("snippet", "").strip()

                # Ignore incomplete search results.
                if not title or not link:
                    continue

                # Ignore duplicate URLs across all research tasks.
                if link in seen_links:
                    continue

                seen_links.add(link)

                evidence.append({
                    "query": query,
                    "query_type": query_type,
                    "engine": engine,
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "source": self._normalize_source(result),
                    "position": result.get("position", 0)
                })

                task_count += 1

        return evidence