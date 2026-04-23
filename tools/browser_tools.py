import json
import os

import requests
from crewai import Agent, LLM, Task
from crewai.tools import tool
from unstructured.partition.html import partition_html

def _crewai_model_from_env() -> str:
  model = os.environ["MODEL"].strip()
  # CrewAI uses LiteLLM under the hood; for Ollama the model is typically `ollama/<model>`.
  if "/" not in model:
    return f"ollama/{model}"
  return model

class BrowserTools():

  scrape_and_summarize_website = None


@tool("Scrape website content")
def scrape_and_summarize_website(website: str) -> str:
  """Useful to scrape and summarize a website content; pass the full URL (no trailing slash)."""
  url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
  payload = json.dumps({"url": website})
  headers = {"cache-control": "no-cache", "content-type": "application/json"}
  try:
    response = requests.request("POST", url, headers=headers, data=payload, timeout=60)
  except requests.RequestException as e:
    return f"\nScrape tool error: request failed ({type(e).__name__}: {e})\n"

  if not response.ok:
    body_preview = (response.text or "").strip()
    if len(body_preview) > 1200:
      body_preview = body_preview[:1200] + "…"
    return (
      "\nScrape tool error: Browserless request failed.\n"
      f"Status: {response.status_code}\n"
      f"Body: {body_preview}\n"
    )

  elements = partition_html(text=response.text)
  content = "\n\n".join([str(el) for el in elements])
  content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
  summaries = []
  for chunk in content:
    agent = Agent(
        role="Principal Researcher",
        goal="Do amazing researches and summaries based on the content you are working with",
        backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
        llm=LLM(
          model=_crewai_model_from_env(),
          base_url=os.getenv("OLLAMA_BASE_URL") or None,
        ),
        allow_delegation=False,
    )
    task = Task(
        agent=agent,
        description=(
          "Analyze and make a LONG summary the content bellow, make sure to include the ALL relevant "
          "information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n"
          f"{chunk}"
        ),
        expected_output="A comprehensive summary of the provided webpage content, including all relevant details and key points.",
    )
    task_output = task.execute_sync()
    summary_text = (
      getattr(task_output, "raw", None)
      or getattr(task_output, "output", None)
      or getattr(task_output, "final_output", None)
      or str(task_output)
    )
    summaries.append(str(summary_text))
    content = "\n\n".join(summaries)
  return f"\nScrapped Content: {content}\n"


# Backwards-compatible alias for older code importing BrowserTools.scrape_and_summarize_website
BrowserTools.scrape_and_summarize_website = staticmethod(scrape_and_summarize_website)
