# Methods and evidence

## Sources

Twenty report years are collected: 2005–2010 and 2012–2025. Report variants and useful appendices are retained. The manifest includes page counts and SHA-256 hashes. One-page letters and identical file contents are excluded. Text extraction covers the first 25 PDF pages, not every table in each full report. The 2021 file has image-based table pages; historical comparisons in later reports supply its figures. No standalone 2002–2004 or 2011 reports are included.

Table E.2 is extracted from 19 report editions into 399 observations, including historical comparisons. A strict Market header determines the year order. Each observation retains filename, PDF page, report edition, units, table and source context. Missing text is not inferred.

## Historical comparisons

For each year and mail market in aggregate data, use the latest available published estimate. This supplies 21 annual observations (2003–2023) per market. Revisions remain traceable; this is not a constant-definition harmonized series. Within-edition comparisons are available. Correspondence, transactions, packages and questionnaires have changed; changes in estimates do not necessarily indicate changes in behavior.

2024–2025 tables use pieces per household per year. Earlier E.2 tables use billions of pieces. These units are never concatenated. Markets describe purpose, not postal product classes. Advertising overlaps other categories; do not add them to reproduce Total. Rounding also affects totals.

## Demographics

The 2025 report Tables 2.2–2.6, PDF pages 16–17, supply 19 groups across age, income, education, homeownership and geography. Received and sent pieces are per household per year. Shares are percentages. Separate marginal groups cannot be combined into joint household profiles. Associations do not establish causation. Large-MSA definitions changed between 2020 and 2025.

## Extractive NLP

Sentences from the first 25 PDF pages of the 2025 report are tokenized with stop-word removal. Token overlap normalized by set sizes supplies similarity weights. A PageRank-style graph algorithm uses 0.85 damping, 25 iterations, topic relevance and diversity filtering to select three sentences for each of nine topics. Quoted passages retain PDF-page links. This is deterministic extractive TextRank, not a generative language model or semantic chatbot. PDF reading-order and extraction errors can remain. Trend summaries are separate arithmetic calculations.

## Forecast evaluation

Train on aggregate observations from 2015–2023. Compare last observation, ordinary least-squares trend, and damped trend (factor 0.8). Select the lowest expanding-window MAE on 2018–2020 validation targets. Evaluate the fixed model choice on separate 2021–2023 targets, training only on earlier target years. Refit on 2015–2023 for projections through 2030. Predictions are clipped at zero.

Historical inputs reflect later report revisions. Evaluation is retrospective and time-ordered, not a real-time archival forecast test. Three validation and three held-out years offer limited evidence, especially across COVID. Both selected-model and naive-baseline errors are displayed; a model may underperform baseline. Shaded bands use maximum held-out absolute error times square root of horizon. They are sensitivity bands, not calibrated confidence intervals.

The cutoff is explicitly 2023. Projections are not updated through 2025. More recent household forecasting needs a harmonized annual per-household dataset. Classification changes limit extrapolation, especially for correspondence and transactions. These are exploratory scenarios, not operational forecasts.

## Verification and impact

Checks cover year/market uniqueness, source paths, unit separation, known table values, demographic coverage, quote provenance and forecast arithmetic. Selected demographic tables are compared with rendered source pages. Browser checks cover tabs, filters, downloads and source access. This is not a manual audit of all values.

The 50% preparation-time reduction is a challenge target, not an achieved result. Validate it with a timed comparison of identical report-writing tasks with and without the dashboard, including errors and user confidence. No results or participants have been invented.
