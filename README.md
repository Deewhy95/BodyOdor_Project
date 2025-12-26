# BodyOdor_Project

A small, reproducible data pipeline and exploratory analysis for a survey on body odor (BO) among residents of Lagos State. The repository contains a Jupyter notebook that documents ingestion, validation, cleaning, and basic exploration of the survey dataset, together with modular Python code for the pipeline steps.

- Author: Adedayo Osifuye
- Last tested: 2025-12-26
- Languages: Jupyter Notebook, Python (pandas)

---

## Table of contents

- [Project overview](#project-overview)
- [Repository structure](#repository-structure)
- [Data](#data)
- [Pipeline modules](#pipeline-modules)
- [Data dictionary (variables)](#data-dictionary-variables)
- [Design decisions & validation rules](#design-decisions--validation-rules)
- [Testing](#testing)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Project overview

This project demonstrates a simple, production-minded pipeline for a small survey dataset about body odor. The goals are:

- Load raw survey data (tab-separated text).
- Validate the presence of expected columns.
- Clean and standardize fields (age groups, LGA names, multi-select fields, binary fields).
- Provide a clean DataFrame ready for exploration and further analysis.
- Document the cleaning choices in a notebook for reproducibility and review.

---

## Repository structure

- BO Data Pipeline.ipynb - Primary Jupyter notebook demonstrating ingestion, validation, cleaning, and some interactive exploration/tests.
- data_ingestion.py - load_data(file_path) utility supporting .csv, .txt, .tsv.
- data_validation.py - validate_columns(df) to confirm required column presence.
- data_cleaning.py - cleaning helpers and clean_dataset(df) for age grouping, LGA standardization/validation, multi-select parsing, and binary mapping.
- Odor_Data.txt - Raw tab-separated survey data (source).
- README.md - This file.

---

## Data

The dataset is a survey with self-reported demographic, hygiene, dietary, sweating, family/medical background, and emotional/social impact questions.

Notes on privacy: the repository contains survey responses. If you plan to publish or share derived data, ensure it is appropriately anonymized and you have the right to redistribute it.

---

## Pipeline modules

- data_ingestion.load_data(file_path)
  - Loads `.csv`, `.txt`, or `.tsv`. For `.txt`/`.tsv` uses tab separator.
- data_validation.validate_columns(df)
  - Confirms all required questions (columns) are present. Prints missing columns if any.
- data_cleaning.clean_dataset(df)
  - Creates ordered Age_Group categorical column (expected groups).
  - Standardizes and validates LGA/LCDA names against a curated list.
  - Parses multi-select fields (Foods, Hygiene, Remedies) into lists.
  - Converts Yes/No/Not sure fields to numeric/binary indicators (e.g., Told_BO, Excessive Sweating).
  - Drops rows with invalid/unknown LGAs (per current implementation) and prints a summary of LGA cleaning.

---


## Data dictionary

The survey questions (columns) include:

1. Age - respondent age group (expected categories: "18-24 years", "25-34 years", "35-44 years", "45-54 years", "55-64 years", "65 & above"). Unexpected values mapped to "Unknown".
2. Gender - respondent gender (string).
3. LGA/LCDA - local government / LCDA (string, standardized by the pipeline).
4. How often do you bathe or shower per day? (string)
5. Do you use any of the following regularly? (multi-select string)
6. How often do you consume the following foods? (multi-select string)
7. Do you sweat excessively even when not active? (Yes/No/Not sure → numeric)
8. Are you aware of any medical condition that may cause body odor? (string)
9. Do you have close relatives with persistent body odor? (string)
10. Have you ever been told you have body odor? (Yes/No/Not sure → numeric)
11. If yes, how did it affect you emotionally? (string)
12. Has body odor ever affected your social life or self-confidence? (string)
13. Do you think body odor can cause social discrimination or stigmatization? (string)
14. Have you tried any of the following to reduce body odor? (multi-select string)
15. Rate the effectiveness of your chosen remedies. (string)
16. Do you believe some people naturally have stronger body odor due to their body chemistry or genetics? (string)
17. Do you think body odor should be treated as a medical issue in some cases (string)

Derived columns added by the pipeline:
- Age_Group - ordered categorical derived from `1. Age`.
- LGA/LCDA - standardized LGA name (validated against a curated list).
- Foods - list parsed from multi-select food responses.
- Hygiene - list parsed from multi-select hygiene responses.
- Remedies - list parsed from multi-select remedies responses.
- Excessive Sweating - numeric mapping of the relevant Yes/No question (1/0/None).
- Told_BO - numeric mapping of whether the respondent has been told they have body odor.

---

## Design decisions & validation rules

- Age group values are forced into a fixed ordered categorical set; unexpected values become "Unknown".
- LGA names are standardized using `standardize_lga()` and validated against a curated `valid_lgas` list in `data_cleaning.py`. Rows with LGAs not in the valid list are currently dropped by `validate_lga()` - this is a conscious choice for data quality in the current pipeline.
- Multi-select fields are parsed by splitting on commas and stripping whitespace.
- Binary-like answers ("Yes"/"No"/"Not sure") are mapped to numeric values for downstream modelling/analysis. "Not sure" is mapped to None (NaN) — treat appropriately in analyses.

---

## Testing

The notebook includes a "Test Code" section that demonstrates a simple end-to-end test of loading, validating, and cleaning. Expected notebook test output (example):

- Data loaded successfully! Shape: (n_rows, n_cols)
- All required columns present.
- LGA Cleaning Summary: { total_rows: X, valid_rows: Y, percent_invalid: Z }
- Cleaning completed successfully! Cleaned Data Shape: (Y, ...)


## Contributing

Contributions are welcome.

## Contact

Repository: https://github.com/Deewhy95/BodyOdor_Project

If you have questions, open an issue in the repo or contact the author via the GitHub profile: Deewhy95.
