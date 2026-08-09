"""MarketIntel MCP server.

Exposes market-research tools (company overview, competitors, product
portfolio, pricing, news) backed by live Tavily web search, plus a
resource listing supported research topics and a reusable competitor
analysis prompt template.
"""

import getpass
import os
from typing import Any, Dict, List, Optional

import keyring # secrets are stored in the OS keychain
from fastmcp import FastMCP
from tavily import TavilyClient


# Looks up a named secret (e.g. an API key) securely instead of hardcoding
# it or storing it in a .env file. Tries the OS keychain first (via the
# `keyring` package); if that's unavailable or the entry isn't found, falls
# back to an environment variable with the same name.
def _get_secret(name: str) -> Optional[str]:
    """Fetch a secret from the OS keychain (preferred), falling back to
    an environment variable of the same name if Keychain lookup fails
    or the entry doesn't exist.
    """
    account = os.environ.get("USER", getpass.getuser())
    try:
        value = keyring.get_password(name, account)
    except Exception:
        value = None
    return value or os.getenv(name)


TAVILY_API_KEY = _get_secret("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError(
        "Missing TAVILY_API_KEY. Store it in your OS keychain with:\n"
        '  security add-generic-password -a "$USER" -s "TAVILY_API_KEY" -w\n'
        "(macOS) or set it as an environment variable before starting the server."
    )




tavily = TavilyClient(api_key=TAVILY_API_KEY)  # Tavily SDK client
mcp = FastMCP(name="MarketIntel")              # FastMCP server scaffold


# Internal helper (not exposed as an MCP tool) that every tool below calls
# into. Sends one query to Tavily's search API and reshapes the raw response
# into a small, consistent dict (query, synthesized answer, cleaned results)
# so every tool returns data in the same predictable shape.
def _tsearch(query: str, **kw) -> Dict[str, Any]:
    """Run a Tavily search and return a clean, structured result."""
    resp = tavily.search(query=query, **kw)
    return {
        "query_used": query,
        "answer": resp.get("answer"),
        "results": [
            {k: r.get(k) for k in ("title", "url", "content", "score", "published_date")}
            for r in resp.get("results", [])
        ],
    }


# MCP resource: a static, read-only reference that clients (Cursor, n8n,
# etc.) can pull to discover what kinds of research this server supports,
# without needing to call any tool or hit the network.
@mcp.resource("resource://market/topics")
def market_topics() -> List[str]:
    """Common market research topics supported by this server."""
    return [
        "Competitor overview",
        "Pricing snapshot",
        "Product portfolio mapping",
        "Market landscape",
        "Feature comparison",
        "Regional GTM",
    ]


# Tool 1: builds a background-check query for one company (founding, HQ,
# products, business model, recent news) and hands it to Tavily. This is
# the baseline info most other research steps build on.
@mcp.tool(annotations={"title": "Company Overview"})
def company_overview(name: str, region: Optional[str] = None, max_results: int = 8):
    """Fetch company background: founding, HQ, products, business model, recent news."""
    reg = f" in {region}" if region else ""
    q = f"Company overview of {name}{reg}: founding, HQ, products, business model, recent news"
    return _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")


# Tool 2: finds a company's rivals, optionally narrowed to a product
# category and/or region, and explicitly asks Tavily to include emerging
# ("upstart") challengers alongside established competitors.
@mcp.tool(annotations={"title": "List Competitors"})
def list_competitors(name: str, category: Optional[str] = None, region: Optional[str] = None, max_results: int = 10):
    """Identify a company's top competitors, optionally filtered by category/region."""
    cat = f" in {category}" if category else ""
    reg = f" in {region}" if region else ""
    q = f"Top competitors of {name}{cat}{reg}; include upstart challengers"
    return _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")


# Tool 3: searches for a company's product/tier/segment lineup, then goes a
# step further than the other tools -- it filters the search results down to
# URLs that look like product/pricing/solutions pages and runs Tavily's
# `extract` on those to pull structured page content (e.g. product tables).
@mcp.tool(annotations={"title": "Product Portfolio Map"})
def product_portfolio(company: str, focus_keywords: Optional[List[str]] = None, max_results: int = 12):
    """Map a company's products, tiers, and service segments, with structured extraction."""
    kws = f" ({', '.join(focus_keywords)})" if focus_keywords else ""
    q = f"{company} product portfolio{kws}: product list, suites, tiers, segments"
    search_res = _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")
    # Keep only result URLs that look like product/pricing/solutions pages,
    # since those are the ones worth extracting full content from.
    product_like = [
        r["url"] for r in search_res.get("results", [])
        if r.get("url") and any(tok in r["url"].lower() for tok in ["product", "products", "pricing", "solutions"])
    ]
    extracted: Dict[str, Any] = {}
    if product_like:
        try:
            extracted = tavily.extract(urls=product_like[:10], extract_depth="advanced", format="markdown")
        except Exception as e:
            # Don't let a failed extraction kill the whole tool call --
            # the search results on their own are still useful.
            extracted = {"error": f"extract_failed: {e}"}
    return {"search": search_res, "extracted": extracted}


# Tool 4: looks up pricing for a specific product or company, optionally
# scoped to a region/currency, asking for list price, tiers, billing
# cycles, discounts, and any hidden fees.
@mcp.tool(annotations={"title": "Pricing Snapshot"})
def pricing_snapshot(product_or_company: str, region: Optional[str] = None, currency_hint: Optional[str] = None, max_results: int = 10):
    """Retrieve pricing details: list price, tiers, billing cycles, discounts, hidden fees."""
    reg = f" in {region}" if region else ""
    cur = f" in {currency_hint}" if currency_hint else ""
    q = f"Pricing for {product_or_company}{reg}{cur}: list price, tiers, billing cycles, discounts, hidden fees"
    return _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")


# Tool 5: pulls the latest company news (funding, acquisitions, product
# launches, leadership changes) within a configurable lookback window,
# using Tavily's "news" topic so results skew toward recent articles.
@mcp.tool(annotations={"title": "Recent News Pulse"})
def recent_news_pulse(company: str, days: int = 30, max_results: int = 10):
    """Surface recent company news: funding, acquisitions, launches, leadership changes."""
    q = f"Recent news about {company}: funding, acquisitions, launches, leadership"
    return _tsearch(q, topic="news", days=days, max_results=max_results, search_depth="advanced", include_answer="advanced")


# MCP prompt: not a tool itself -- it returns instruction text that guides
# an LLM client to call the five tools above in a consistent order and
# assemble the results into a structured competitor brief.
@mcp.prompt
def competitor_analysis_prompt(company: str, region: str = "", category: str = "") -> str:
    """Reusable template that guides a structured competitor brief."""
    return (
        f"Build a competitor brief for '{company}'"
        + (f" in '{region}'" if region else "")
        + (f" within '{category}'" if category else "")
        + ". Steps: 1) Company Overview 2) List Competitors 3) Portfolio & Pricing 4) News Pulse 5) SWOT+Five Forces."
    )


# Entry point: starts the MCP server over SSE transport so clients like
# Cursor or n8n can connect to it at http://127.0.0.1:8000/sse.
def main():
    print("\n🚀 Starting MarketIntel MCP Server...")
    mcp.run(transport="sse")  # Cursor connects at http://127.0.0.1:8000/sse


if __name__ == "__main__":
    main()
