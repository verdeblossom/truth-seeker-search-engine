import sys
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# ===================================================================
# IMPROVED TRUTH-SEEKING HEURISTICS (v2) — Supreme Directive Edition
# ===================================================================
# Purely mechanical, inspectable rules grounded in objective signals:
#   • Official government/academic/international domains
#   • Peer-reviewed scientific publishers
#   • Wire services with top factual ratings
#   • Primary source indicators (.pdf, DOI, reports)
#   • Targeted penalties only for sensationalist/low-credibility domains

TRUST_BOOST = {
    # Highest tier — official records
    '.gov': 25, '.mil': 25, '.int': 20,
    # Academia (US + international)
    '.edu': 22, '.ac.uk': 20,
    # Wire services — consistently highest factual reporting
    'reuters.com': 18, 'apnews.com': 18,
    # Major government & health/science agencies
    'nih.gov': 28, 'cdc.gov': 28, 'nasa.gov': 28,
    'who.int': 25, 'epa.gov': 25, 'noaa.gov': 25,
    'fda.gov': 25, 'census.gov': 25, 'science.gov': 25,
    # Top peer-reviewed & research publishers
    'nature.com': 22, 'science.org': 22, 'pnas.org': 22,
    'arxiv.org': 21, 'pubmed.ncbi.nlm.nih.gov': 22,
    'thelancet.com': 22, 'nejm.org': 22, 'jamanetwork.com': 22,
    'plos.org': 20,
    # Reputable reference / encyclopedic
    'wikipedia.org': 10,
}

PRIMARY_SOURCE_INDICATORS = {
    '.pdf': 12,          # Direct documents
    'doi.org': 15,       # Digital Object Identifier = peer-reviewed
    '/report': 8,
    '/data': 8,
    'study': 6,          # Snippet signals
    'official report': 8,
    'peer-reviewed': 7,
}

PENALTY_DOMAINS = {
    # Sensationalist / repeatedly low-factual (non-partisan selection)
    'infowars.com': -12,
    'naturalnews.com': -12,
    'breitbart.com': -8,
    'dailymail.co.uk': -7,
    # Social media / aggregator noise
    'twitter.com': -5,
    'x.com': -5,
    'facebook.com': -5,
    'reddit.com': -4,
}

def truth_score(result):
    url = result.get('href', '').lower()
    if not url:
        return 0
    domain = urlparse(url).netloc.lower()
    snippet = result.get('body', '').lower()
    title = result.get('title', '').lower()

    score = 0

    # 1. TLD & exact-domain boosts
    for key, boost in TRUST_BOOST.items():
        if key in domain:
            score += boost

    # 2. Primary-source URL & snippet signals
    for indicator, boost in PRIMARY_SOURCE_INDICATORS.items():
        if indicator in url or indicator in snippet or indicator in title:
            score += boost

    # 3. Penalties for low-credibility / noise domains
    for bad_domain, penalty in PENALTY_DOMAINS.items():
        if bad_domain in domain:
            score += penalty
            break

    # 4. Small recency nudge (DuckDuckGo already favors recent; we reinforce)
    if any(year in snippet or year in title for year in ['2025', '2026', '2024']):
        score += 3

    return max(score, 0)  # Never go negative


def main():
    if len(sys.argv) < 2:
        query = input("Enter your search query: ").strip()
    else:
        query = ' '.join(sys.argv[1:])

    if not query:
        print("No query provided.")
        return

    print(f"\n🔎 Searching for: {query}")
    print("   (v2 truth-seeking re-ranking — primary sources + official/academic priority)\n")

    with DDGS() as ddgs:
        raw_results = list(ddgs.text(query, max_results=30, safesearch="moderate"))

    # Re-rank
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
