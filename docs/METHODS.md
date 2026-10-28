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


## January 2025 survey break (verified)

FY2025 HMS Appendix B, PDF page 75 (printed p. 65), says the redesign and name change began in January 2025. FY2025 therefore combines Oct–Dec 2024 under the previous design with Jan–Sep 2025 under the new one; the report's 2015 and 2020 comparisons use the old design. The new design uses residential-address sampling with specified exclusions and strata targeting lower-income/renter areas (p. 75), and web or telephone-assisted collection (p. 76). The old design offered both paper and online diaries (FY2024 report, PDF pp. 80–82). It would be inaccurate to describe the earlier survey as paper-only or to assert a quantitatively wider sampling frame without evidence. Collection, sampling and weighting changed; observed differences need not be entirely behavioral.

FY2025 Appendix B, PDF p. 80, documents the Large MSA expansion from the 30 largest metros to metropolitan areas with at least one million people in January 2025. About 11% of households shift from Other MSA to Large MSA. FY2025 is a hybrid of old/new definitions. MSA classification is not a rural/urban indicator.

## Demographic comparisons added for the showcase

Table 2.7, FY2025 PDF p. 18, provides six age groups' shares of mail and shares of households in 2015/2020/2025 (36 observations). Its row measures are percentages despite the printed table's pieces-per-household subtitle. Table 7.2, PDF p. 52, provides packages received by Large MSA, Other MSA and Non-MSA for those years (nine observations). Both tables retain source edition 2025, table number, page and units. The app does not infer missing historical received/sent mail volumes from age shares. Non-MSA packages received are 19.7, 43.4 and 50.0; Large MSA are 33.4, 41.3 and 32.8. These published comparisons span both method and classification changes.

## Coverage follow-up

The supplied FY2011 PDF URL returned HTTP 404 during this check. The official HTML report remains a reference, but no PDF was added and existing historical estimates were unchanged. A focused official-source search did not locate the FY2003 report cheaply. Neither gap was filled with inferred values.

## Hosting and exports

GitHub Pages serves main at /. All runtime assets use relative paths. Brief exports resolve source PDF/page URLs against the current site location and include all selected trend rows, units, source editions and pages, the forecast caveat, and selected exact passages. The exported arithmetic and extracts are not generated explanations. URL hash state is allow-listed and validated against available options. dashboard.html redirects old bookmarks to index.html.
