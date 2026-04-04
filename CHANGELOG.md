# Changelog

All notable changes to the Truth-Seeking Search Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Support for the new `ddgs` package (replaces old `duckduckgo-search`)
- Increased default results to 40 for richer output
- Minor heuristic improvements (e.g., light boosts for math/educational content)

### Changed
- Updated import from `duckduckgo_search` to `ddgs`
- Script renamed/restructured to `truth-search-v3.py` (or your preferred name)
- Improved installation instructions

### Fixed
- Removed RuntimeWarning related to package rename

## [v2.0.0] - 2026-04-04
### Added
- v2 truth-seeking heuristics with primary source detection (.pdf, DOI, reports)
- Score breakdown display for transparency

## [v1.0.0] - Initial Release
### Added
- Basic DuckDuckGo search with rule-based truth-seeking re-ranking
- Boosts for .gov, .edu, scientific domains
- Penalties for low-credibility sites
