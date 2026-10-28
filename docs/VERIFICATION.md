# Verification — 28 October 2026

- `python -m unittest discover -s tests`: 11 tests passed. Includes source-file/page coverage for every plotted observation and projection training point, historical comparisons, presentation figures, and static entry assets.
- Browser checks: 478 filter views across 1280×720 and 1920×1080; no horizontal overflow, error alerts or invalid SVG coordinates. Keyboard tab navigation and filter URL restoration passed.
- Downloaded and opened annual, snapshot, historical comparison and forecast CSV exports, plus the Markdown evidence brief.
- Checked 375 visible text samples across all five sections after the final palette change. Lowest measured contrast was 5.24:1. This is a focused contrast/keyboard check, not a complete accessibility certification.
- Reference figures unchanged: 97.4 billion pieces (2023), 637.3 pieces/household (2025), 346.9 received (under 35), 874.4 received (75+), held-out MAE 4.49 versus baseline 4.40.
- Added 45 published historical demographic observations from FY2025 Tables 2.7 and 7.2. These are comparisons across changing methods, not a harmonized series. January 2025 survey and metro-definition changes are disclosed.
- No standalone 2011 PDF added: the supplied official PDF URL returned 404. FY2003 was not found in the limited official-source search; further collection intentionally deferred. Existing coverage limits remain.
- The second physical showcase laptop and a physical projector were unavailable. The team must rehearse on both devices before November 7.
- Desktop scope retained; no framework, build step, runtime dependency, cloud service or model call added. Presentation remains a separate file outside the repository.
