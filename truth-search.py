import sys
from urllib.parse import urlparse
from ddgs import DDGS  # Updated import for the current package

# ===================================================================
# TRUTH-SEEKING HEURISTICS v3 — Supreme Directive Edition
# ===================================================================
# Pure rule-based, inspectable signals prioritizing objective reality

TRUST_BOOST = {
    # Official & academic
    '.gov': 25, '.mil': 25, '.int': 20, '.edu': 22, '.ac.uk': 20,
    # Wire services & top science
    'reuters.com': 18, 'apnews.com': 18,
    'nih.gov': 28, 'cdc.gov': 28, 'nasa.gov': 28, 'who.int': 25,
    'nature.com': 22, 'science.org': 22, 'arxiv.org': 21,
    'pubmed.ncbi.nlm.nih.gov': 22, 'mit.edu': 20,  # Added for strong academic hits
    # Reference / encyclopedic
    'wikipedia.org': 12,
}

PRIMARY_SOURCE_INDICATORS = {
    '.pdf': 12, 'doi.org': 15, '/report': 8, '/data': 8,
    'study': 6, 'official report': 8, 'peer-reviewed': 7,
    'mathematics': 5, 'equation': 5,  # Light boost for math grounding
}

PENALTY_DOMAINS = {
    'infowars.com': -12, 'naturalnews.com': -12,
    'breitbart.com': -8, 'dailymail.co.uk': -7,
    'twitter.com': -5, 'x.com': -5, 'facebook.com': -5,
    'reddit.com': -4, 'quora.com': -3,  # Mild penalty for discussion forums
}

def truth_score(result):
    url = result.get('href', '').lower()
    if not url:
        return 0
    domain = urlparse(url).netloc.lower()
    snippet = result.get('body', '').lower()
    title = result.get('title', '').lower()

    score = 0

    # TLD & domain boosts
    for key, boost in TRUST_BOOST.items():
        if key in domain:
            score += boost

    # Primary-source & content signals
    for indicator, boost in PRIMARY_SOURCE_INDICATORS.items():
        if indicator in url or indicator in snippet or indicator in title:
            score += boost

    # Penalties
    for bad_domain, penalty in PENALTY_DOMAINS.items():
        if bad_domain in domain:
            score += penalty
            break

    # Recency nudge
    if any(year in snippet or year in title for year in ['2024', '2025', '2026']):
        score += 3

    return max(score, 0)


def main():
    if len(sys.argv) < 2:
        query = input("Enter your search query: ").strip()
    else:
        query = ' '.join(sys.argv[1:])

    if not query:
        print("No query provided.")
        return

    print(f"\n🔎 Searching for: {query}")
    print("   (v3 truth-seeking re-ranking — primary sources + official/academic priority)\n")

    with DDGS() as ddgs:
        raw_results = list(ddgs.text(query, max_results=40, safesearch="moderate"))

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
