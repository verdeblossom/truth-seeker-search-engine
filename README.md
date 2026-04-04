# Truth-Seeking Search Engine

A minimal, no-AI Python script that searches via DuckDuckGo and **re-ranks** results using transparent, rule-based heuristics prioritizing grounding in objective reality (.gov, .edu, scientific sources, primary documents). No generated summaries, no black-box AI.

**See the [CHANGELOG.md](https://github.com/verdeblossom/truth-seeker-search-engine/edit/main/CHANGELOG.md) for full version history and changes.**


## Installation

```bash

pip install ddgs

```

## Usage

**Console Version** (fast, for quick terminal searches)

```bash

python truth-search.py "your query here"

```

**GUI Version** (Recommended — opens in browser with clickable links)

```bash

streamlit run truth-search-gui.py

```

After running the GUI command, a browser window will automatically open.

## Features

- Pure rule-based truth-seeking ranking (no AI involved)

- Strong priority for official, academic, and primary sources

- Penalties for low-credibility and noisy domains

- Fully transparent scoring shown on each result

- Works entirely locally after the initial search

---

Built with the objective, truth-seeking researcher in mind. Fork it, tweak the heuristics, make it your own.

```

