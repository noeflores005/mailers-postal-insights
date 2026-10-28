# Mailers final presentation — four-minute script

Before the event: fill in team member names if desired, rehearse at normal speaking speed and bring the entire project folder on both laptops. Open index.html before connecting the projector. The schedule allows one minute setup, four minutes presentation and two minutes questions. Keep screenshots in demo/ as backup.

## Slides 1–2 · 0:00–0:20

We are team Mailers. Our project is Postal Insights, a local dashboard for understanding how American households use mail. We built it for the USPS Office of Inspector General challenge: make dense annual survey reports easier to explore and turn their evidence into useful comparisons.

## Slide 3 · 0:20–0:45

The information exists across many annual PDFs, but finding comparable values is difficult. Some newer reports revise historical figures, and the newest summaries switch from billions of pieces to pieces per household. A chart that silently joins those numbers can look convincing and still be misleading. Our approach makes those differences visible and keeps every plotted value connected to its source.

## Slide 4 · 0:45–1:10

The dashboard has five sections: historical trends, household comparisons, a forecast lab, report insights, and sources and methods. We collected twenty report years and structured Table E.2 from nineteen editions. Historical comparison columns also give us annual observations back to 2003. Everything runs locally, including the charts and extractive summaries, without a cloud service or API key.

## Slide 5 · 1:10–1:40

Our workflow copies the full reports, extracts text, structures tables and records the filename, edition, units and PDF page. For the long-term view we choose the latest available historical estimate. Because questionnaire and classification changes remain, this is not a fully harmonized series; we also provide within-edition comparisons. The NLP feature uses topic-weighted TextRank to select relevant source sentences. It quotes the report rather than inventing an explanation.

## Slide 6 · 1:40–2:10

The forecast lab compares a last-observation baseline, a linear trend and a damped trend. We select on 2018 through 2020 validation years and evaluate separately on 2021 through 2023. The total-mail model has a held-out mean absolute error of 4.49 billion pieces, compared with 4.40 for the simple baseline. It did not outperform the baseline, and we display that result. The projections are exploratory scenarios frozen at 2023; the shaded bands are sensitivity bands, not confidence intervals.

## Slide 7 · 2:10–3:30 · Live demonstration

Open Mail over time. The total series shows 97.4 billion pieces for 2023, with a source link behind each point. Switch to a single report edition and choose 2025: the unit changes to pieces per household per year, and the published total is 637.3. These values stay separate.

Open Who uses mail. In 2025, households headed by someone under 35 received 346.9 pieces per year, while those headed by someone 75 or older received 874.4. Switch to income or ownership to see another survey breakdown. These are associations, not causal estimates or joint household filters.

Open From the reports and choose a topic. Each selected passage links to the actual PDF page. Finally, open Looking ahead and point to the held-out error and baseline comparison. Export a CSV if time allows. If anything fails, show the matching screenshots from demo/.

## Slides 8–9 · 3:30–4:00

The value is a shorter path from a question to an auditable table, comparison and draft evidence brief. We have not measured the challenge’s fifty-percent preparation-time target. The next evaluation would time the same reporting task with and without this dashboard and check both speed and accuracy. Our main next data step is harmonizing classifications and building a consistent annual per-household series for more current forecasting. Thank you; we welcome your questions.

## Judge questions

**Is the summarizer generative AI?** No. It is local extractive NLP using graph ranking, not an LLM. It selects and quotes report sentences. Arithmetic summaries are separate.

**Why does the forecast stop training at 2023?** The latest extracted E.2 reports switch units. We retain those reports separately rather than introduce an unsupported conversion. Forecast scenarios can extend to 2030, but they remain based on a 2023 cutoff.

**Did your model beat a simple baseline?** The total-mail model did not. Both held-out errors are visible. Three held-out years and source revisions limit the evaluation.

**Did you achieve the fifty-percent goal?** We have not run a timed user study. It is the target for a follow-up evaluation, not a measured outcome.

**Can I filter by exact USPS product?** The current historical view uses mail-market purpose from E.2. It does not provide a full postal-product taxonomy. That would require additional source-table extraction and mapping.

**Are all years fully digitized?** No. We have full report files, but structured extraction focuses on summary E.2 tables and FY2025 demographic tables. The source library describes the scope and image-based pages.
