```python
import streamlit as st
from urllib.parse import urlparse
from ddgs import DDGS

# ===================================================================
# TRUTH-SEEKING HEURISTICS v3 (same as console version)
# ===================================================================
TRUST_BOOST = {
    '.gov': 25, '.mil': 25, '.int': 20, '.edu': 22, '.ac.uk': 20,
    'reuters.com': 18, 'apnews.com': 18,
    'nih.gov': 28, 'cdc.gov': 28, 'nasa.gov': 28, 'who.int': 25,
    'nature.com': 22, 'science.org': 22, 'arxiv.org': 21,
    'pubmed.ncbi.nlm.nih.gov': 22, 'mit.edu': 20,
    'wikipedia.org': 12,
}

PRIMARY_SOURCE_INDICATORS = {
    '.pdf': 12, 'doi.org': 15, '/report': 8, '/data': 8,
    'study': 6, 'official report': 8, 'peer-reviewed': 7,
    'mathematics': 5, 'equation': 5,
}

PENALTY_DOMAINS = {
    'infowars.com': -12, 'naturalnews.com': -12,
    'breitbart.com': -8, 'dailymail.co.uk': -7,
    'twitter.com': -5, 'x.com': -5, 'facebook.com': -5,
    'reddit.com': -4, 'quora.com': -3,
}

def truth_score(result):
    url = result.get('href', '').lower()
    if not url:
        return 0
    domain = urlparse(url).netloc.lower()
    snippet = result.get('body', '').lower()
    title = result.get('title', '').lower()
    score = 0
    for key, boost in TRUST_BOOST.items():
        if key in domain:
            score += boost
    for indicator, boost in PRIMARY_SOURCE_INDICATORS.items():
        if indicator in url or indicator in snippet or indicator in title:
            score += boost
    for bad_domain, penalty in PENALTY_DOMAINS.items():
        if bad_domain in domain:
            score += penalty
            break
    if any(year in snippet or year in title for year in ['2024', '2025', '2026']):
        score += 3
    return max(score, 0)

# ====================== STREAMLIT GUI ======================
st.set_page_config(page_title="Truth-Seeking Search", page_icon="🔎")
st.title("🔎 Truth-Seeking Search Engine")
st.caption("Re-ranked by grounding in objective reality • No AI summaries")

query = st.text_input("Enter your search query:", placeholder="causes of the 2008 financial crisis")

if st.button("Search") and query:
    with st.spinner("Searching and re-ranking by truth-seeking heuristics..."):
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=40, safesearch="moderate"))
        
        ranked = sorted(raw_results, key=truth_score, reverse=True)
        
        st.success(f"Top {len(ranked)} results (re-ranked by objective reality):")
        
        for i, r in enumerate(ranked, 1):
            title = r.get('title', 'No title')
            url = r.get('href', '#')
            snippet = r.get('body', 'No snippet available')
            score = truth_score(r)
            
            st.markdown(f"**{i}. [{score}]** [{title}]({url})")
            st.caption(url)
            st.write(snippet[:280] + "..." if len(snippet) > 280 else snippet)
            st.divider()
