import json
import os

import requests
from crewai.tools import tool


def _search(query: str, n_results: int = 5) -> str:
  url = "https://google.serper.dev/search"
  payload = json.dumps({"q": query})
  headers = {
      "X-API-KEY": os.environ["SERPER_API_KEY"],
      "content-type": "application/json",
  }
  try:
    response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
  except requests.RequestException as e:
    return f"\nSearch tool error: request failed ({type(e).__name__}: {e})\n"

  if not response.ok:
    body_preview = (response.text or "").strip()
    if len(body_preview) > 800:
      body_preview = body_preview[:800] + "…"
    return (
      "\nSearch tool error: Serper request failed.\n"
      f"Status: {response.status_code}\n"
      f"Body: {body_preview}\n"
    )

  try:
    data = response.json()
    results = data.get("organic", [])
  except ValueError:
    body_preview = (response.text or "").strip()
    if len(body_preview) > 800:
      body_preview = body_preview[:800] + "…"
    return (
      "\nSearch tool error: Serper returned non-JSON response.\n"
      f"Status: {response.status_code}\n"
      f"Body: {body_preview}\n"
    )

  stirng = []
  for result in results[:n_results]:
    try:
      stirng.append("\n".join([
          f"Title: {result['title']}",
          f"Link: {result['link']}",
          f"Snippet: {result['snippet']}",
          "\n-----------------",
      ]))
    except KeyError:
      continue

  content = "\n".join(stirng)
  return f"\nSearch result: {content}\n"


@tool("Search internet")
def search_internet(query: str) -> str:
  """Useful to search the internet about a given topic and return relevant results."""
  return _search(query)

@tool("Search instagram")
def search_instagram(query: str) -> str:
  """Useful to search for instagram post about a given topic and return relevant results."""
  query = f"site:instagram.com {query}"
  return _search(query)

class SearchTools:
  # Backwards-compatible aliases (older code imports class methods).
  search_internet = staticmethod(search_internet)
  search_instagram = staticmethod(search_instagram)

