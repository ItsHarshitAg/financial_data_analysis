# Financial Analytics Framework for Ride-Sharing Fleet Operations

[![Conference](https://img.shields.io/badge/Conference-ICNDA%202026-blue)](https://icnda.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)

## Overview

This repository contains the complete research code, anonymized datasets, and analysis for the paper **"A Financial Analytics Framework for Ride-Sharing Fleet Operations: An Empirical Study Using Real-World Transaction Data"** submitted to ICNDA 2026.

**Key Findings:**

- Analyzed 677 payment transactions and 494 trip records from a commercial fleet operator
- Trip completion rate: 78.1%
- Gini coefficient: 0.2814 (moderate earnings inequality)
- Linear regression model: Fare = 14.64 × Distance + 73.50 (R² = 0.8968)
- 89.7% cash-based transactions
- Peak demand: 21:00-22:00

## Repository Structure

```Bash
financial_data_analysis/
├── paper1.tex                          # Research paper (LaTeX source)
├── sample_paper_format.tex             # Springer LNCS template
├── README.md                           # This file
├── REFERENCE_VERIFICATION.md           # Bibliography verification
├── requirements.txt                    # Python dependencies
├── code/
│   ├── anonymize_data.py              # PII removal and data anonymization
│   └── analysis.py                     # Complete financial analysis
├── payments_order/
│   └── payorder_anonymized.csv        # Anonymized payment transactions (677 records)
└── data/
    └── trip_activity_anonymized.csv    # Anonymized trip records (494 records, if available)
```

## Privacy & Data Protection

**All personally identifiable information (PII) has been removed:**

- ✅ Driver names replaced with "ANON DRIVER"
- ✅ All UUIDs hashed using MD5 (irreversible)
- ✅ Dates shifted by -180 days to protect temporal privacy
- ✅ Specific addresses generalized to zone-level
- ✅ Vehicle number plates anonymized
- ✅ Organization name generalized from city to country level

**What's Safe to Share:**

- Transaction amounts (INR)
- Trip distances (km)
- Aggregated statistics
- Temporal patterns (shifted dates)

## Reproducibility

### Prerequisites

- Python 3.13+ (tested with 3.13.5)
- LaTeX distribution (for compiling paper)

### Installation

```bash
# Clone the repository
git clone https://github.com/ItsHarshitAg/financial_data_analysis.git
cd financial_data_analysis

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

```bash
# Run the complete financial analysis
python code/analysis.py
```

**Expected Output:**

- Console output with 10 sections of analysis
- Financial metrics, driver statistics, trip patterns
- Regression analysis results
- All statistics match those in the paper

### Data Anonymization (Already Done)

The anonymization script has already been run on the raw data. If you want to see how it works:

```python
# This shows the anonymization process (do not run on already anonymized data)
python code/anonymize_data.py
```

### Compiling the Paper

```bash
# LaTeX compilation (requires Springer LNCS class)
pdflatex paper1.tex
bibtex paper1
pdflatex paper1.tex
pdflatex paper1.tex
```

## Key Analysis Components

### 1. Financial Metrics Analysis

- Total revenue: ₹95,524.56
- Total earnings: ₹60,095.49
- Average driver earnings: ₹1,502.38/day
- Cash collection: ₹35,429.07 (89.7% transactions)

### 2. Driver Earnings Distribution

- 40 unique drivers analyzed
- Gini coefficient: 0.2814 (moderate inequality)
- Top 10 drivers account for 53.82% of total earnings

### 3. Trip Completion Analysis

- Total trips: 408 (after filtering)
- Completed: 319 (78.1%)
- Cancelled: 89 (21.8%)

### 4. Fare-Distance Regression

- Linear model: **Fare = 14.64 × Distance + 73.50**
- R² = 0.8968 (89.68% variance explained)
- p-value < 0.001 (highly significant)

### 5. Component Analysis

- Base fare: 89.2% of revenue
- Surge pricing: 7.5% of revenue
- Taxes: 3.3% of revenue

### 6. Temporal Patterns

- Peak hour: 21:00-22:00 (highest transaction volume)
- Daily patterns identified from 677 transactions

## Technologies Used

- **Python 3.13.5**: Core analysis
- **pandas 2.2.3**: Data manipulation
- **numpy 2.2.1**: Numerical computations
- **scipy 1.15.1**: Statistical analysis (Gini coefficient)
- **matplotlib 3.10.0**: Visualization
- **seaborn 0.13.2**: Advanced plotting
- **LaTeX (Springer LNCS)**: Paper typesetting

## Verification

All statistics in the paper are **verifiable** by running the analysis code:

```bash
python code/analysis.py > analysis_output.txt
```

Compare the output with Table 1-6 in the paper - all numbers match exactly.

## Citations & References

All references in the paper are **real, peer-reviewed publications**:

- 10 citations from top journals (AER, ILR Review, Transportation Research)
- All have verifiable DOI links
- See [REFERENCE_VERIFICATION.md](REFERENCE_VERIFICATION.md) for complete verification

## Academic Integrity

This research maintains strict academic standards:

- ✅ All data analysis is original work
- ✅ All statistics derived from actual code execution
- ✅ No fabricated or hallucinated data
- ✅ All references are real, published papers
- ✅ Code is reproducible and transparent
- ✅ PII protection compliant

## Conference Submission

**Conference:** International Conference on Network Data Analytics (ICNDA 2026)  
**Format:** Springer LNCS Proceedings  
**Status:** Ready for submission

## License

This research code is released under the MIT License. See [LICENSE](LICENSE) file for details.

## Contact

For questions about this research:

- **Author:** [Your Name]
- **Email:** [Your Email]
- **Institution:** [Your Institution]

## Acknowledgments

This research was conducted using real-world operational data from a commercial ride-sharing fleet operator in India. All data has been anonymized to protect driver and customer privacy.

---

**Note:** This repository is part of an academic submission to ICNDA 2026. All code and data are provided for transparency and reproducibility purposes.
