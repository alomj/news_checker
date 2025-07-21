from ddgs import DDGS


def search_news(query: str):
    with DDGS() as ddgs:
        return list(ddgs.news(query, max_search=5))
