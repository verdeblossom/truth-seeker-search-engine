import sys
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# ===================================================================
# TRUTH-SEEKING RANKING HEURISTICS (the "supreme directive" engine)
# ===================================================================
# These are purely mechanical rules grounded in observable reality:
#   - .gov / .mil / .edu = highest weight (official records, academia)
#   - Scientific & research orgs = very high
#   - Primary sources & established institutions = high
#   - News/blogs with heavy editorial slant or known low factual reliability = penalized
#   - Everything else is neutral

TRUST_BOOST = {
    # Government & official records
    '.gov': 20, '.mil': 20,
    # Academia & research
    '.edu': 18,
    # Major scientific & standards bodies
    'nih.gov': 22, 'cdc.gov': 22, 'nasa.gov': 22,
    'who.int': 20, 'nature.com': 18, 'science.org': 18,
    'arxiv.org': 17, 'pubmed.ncbi.nlm.nih.gov': 17,
    # Established encyclopedic / primary reference
    'wikipedia.org': 12,
    # Major peer-reviewed publishers
    'elsevier.com': 15, 'springer.com': 15, 'ieee.org': 15,
}

PENALTY_DOMAINS = {
    # Heavily sensationalist or repeatedly low-credibility domains
    # (only a few examples; you can expand this list yourself)
    'breitbart.com': -8, 'infowars.com': -12,
    'naturalnews.com': -10, 'dailymail.co.uk': -6,
    # Add more if you wish — the list is user-editable
}

def truth_score(result):
    url = result.get('href', '')
    if not url:
        return 0
    domain = urlparse(url).netloc.lower()
    score = 0

    # TLD & exact domain boosts
    for key, boost in TRUST_BOOST.items():
        if key in domain:
            score += boost

    # Penalty for known low-credibility domains
    for bad_domain, penalty in PENALTY_DOMAINS.items():
        if bad_domain in domain:
            score += penalty
            break

    # Small recency bonus (DuckDuckGo already surfaces recent results;
    # we just give an extra nudge to anything with a clear date)
    snippet = result.get('body', '').lower()
    if any(word in snippet for word in ['2024', '2025', '2026']):
        score += 2

    return score


def main():
    if len(sys.argv) < 2:
        query = input("Enter your search query: ").strip()
    else:
        query = ' '.join(sys.argv[1:])

    if not query:
        print("No query provided.")
        return

    print(f"\n🔎 Searching for: {query}")
    print("   (truth-seeking re-ranking active — no AI summaries)\n")

    with DDGS() as ddgs:
        raw_results = list(ddgs.text(query, max_results=30, safesearch="moderate"))

    # Re-rank using the objective-reality score
    ranked = sorted(raw_results, key=truth_score, reverse=True)

    print(f"Top {len(ranked)} results (re-ranked by grounding in objective reality):\n")
    for i, r in enumerate(ranked, 1):
        title = r.get('title', 'No title')
        url = r.get('href', 'No URL')
        snippet = r.get('body', 'No snippet available')
        score = truth_score(r)
        print(f"{i:2d}. [{score:3d}] {title}")
        print(f"    {url}")
        print(f"    {snippet[:280]}..." if len(snippet) > 280 else f"    {snippet}")
        print("-" * 80)


if __name__ == "__main__":
    main()
