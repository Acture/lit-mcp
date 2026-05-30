import sys
import time
import requests
from typing import List, Dict, Any

def find_dblp_publications(query: str, max_results: int = 10, max_retries: int = 4) -> List[Dict[str, Any]]:
    """Search DBLP database for computer science papers.
    
    Retries on rate limiting (HTTP 429) and transient server errors with
    exponential backoff. If the request keeps failing it raises RuntimeError
    rather than returning an empty list, so callers can tell a failed search
    apart from a search that genuinely found nothing.

    Args:
        query: The search query string
        max_results: Maximum number of results to return
        max_retries: How many times to retry before giving up

    Returns:
        List of dictionaries with publication data including:
        - authors: List of author names
        - title: Publication title
        - venue: Publication venue
        - volume: Volume number
        - number: Publication number
        - pages: Page numbers
        - publisher: Publisher name
        - year: Publication year
        - type: Publication type
        - access: Access type
        - key: DBLP key
        - doi: DOI identifier
        - ee: Electronic edition link
        - url: DBLP page URL
    """
    # DBLP API endpoint
    url = f"https://dblp.org/search/publ/api"
    params = {
        'q': query,
        'format': 'json',
        'h': max_results
    }
    # DBLP asks clients to identify themselves and throttles anonymous ones.
    headers = {
        'User-Agent': 'lit-mcp (literature-search MCP; https://github.com/gauravfs-14/lit-mcp)',
        'Accept': 'application/json',
    }

    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)

            # 429 (rate limited) and 503 are temporary; wait and try again.
            if response.status_code in (429, 503):
                retry_after = response.headers.get('Retry-After', '')
                delay = float(retry_after) if retry_after.isdigit() else 2 ** attempt
                last_error = f"HTTP {response.status_code}"
                _log(f"DBLP returned {response.status_code} for {query!r}; retrying in {delay:.0f}s")
                time.sleep(min(delay, 30))
                continue

            response.raise_for_status()
            data = response.json()
            return _parse_publications(data)

        except requests.RequestException as e:
            last_error = e
            delay = 2 ** attempt
            _log(f"DBLP request failed for {query!r}: {e}; retrying in {delay:.0f}s")
            time.sleep(min(delay, 30))

    # Out of retries: surface the failure instead of pretending there were no results.
    raise RuntimeError(f"DBLP search failed for {query!r} after {max_retries} attempts (last error: {last_error})")


def _log(message: str) -> None:
    # Log to stderr: stdout is the JSON-RPC channel for stdio MCP servers,
    # so anything written there would break the protocol.
    print(message, file=sys.stderr, flush=True)


def _parse_publications(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Extract publications from the response
    publications = []
    if 'result' in data and 'hits' in data['result'] and 'hit' in data['result']['hits']:
        hits = data['result']['hits']['hit']

        # Ensure hits is a list
        if not isinstance(hits, list):
            hits = [hits]

        for hit in hits:
            info = hit.get('info', {})

            # Extract authors. DBLP returns each author as an object like
            # {'@pid': ..., 'text': 'Name'}, so pull out the name string.
            authors = []
            if 'authors' in info and 'author' in info['authors']:
                author_data = info['authors']['author']
                if not isinstance(author_data, list):
                    author_data = [author_data]
                authors = [a.get('text', '') if isinstance(a, dict) else a for a in author_data]

            # Create publication dictionary
            publication = {
                'title': info.get('title', ''),
                'authors': authors,
                'venue': info.get('venue', ''),
                'volume': info.get('volume', ''),
                'number': info.get('number', ''),
                'pages': info.get('pages', ''),
                'publisher': info.get('publisher', ''),
                'year': info.get('year', ''),
                'type': info.get('type', ''),
                'access': info.get('access', ''),
                'key': info.get('key', ''),
                'doi': info.get('doi', ''),
                'ee': info.get('ee', ''),
                'url': info.get('url', '')
            }

            publications.append(publication)

    return publications