# Financial Analytics Framework for Ride-Sharing Fleet Operations

## ICNDA 2026 Conference Paper

This repository contains the code, anonymized data, and analysis for the research paper:

### "A Financial Analytics Framework for Ride-Sharing Fleet Operations: An Empirical Study Using Real-World Transaction Data"

---

## Repository Structure

```bash
├── paper1.tex                    # Research paper (LaTeX - Springer format)
├── sample_paper_format.tex       # Springer template reference
├── README.md                     # This file
├── code/
│   ├── anonymize_data.py         # PII removal script
│   └── analysis.py               # Comprehensive data analysis
├── payments_order/
│   ├── payorder.csv              # Original data (with PII - NOT for sharing)
│   └── payorder_anonymized.csv   # Anonymized payment data
└── trip_activity/
    ├── [original].csv            # Original data (with PII - NOT for sharing)
    └── trip_activity_anonymized.csv  # Anonymized trip data
```

---

## Data Description

### Payment Transactions Dataset

- **Records**: 677 transactions
- **Key Fields**: Transaction ID, Driver ID, Fare components, Tips, Tolls, Taxes
- **Time Period**: Shifted for anonymization

### Trip Activity Dataset

- **Records**: 494 trips
- **Key Fields**: Trip ID, Distance, Duration, Status, Service Type, Fare
- **Location**: Chennai Metro Area (zones only, addresses anonymized)

---

## Privacy & Anonymization

All personally identifiable information (PII) has been removed:

|Original Data|Anonymized As|
|---------------|---------------|
|Driver names|Anonymous IDs (DRIVER_XXXXXXXX)|
|UUIDs|Hash-based IDs|
|Number plates|Anonymous vehicle IDs|
|Detailed addresses|Zone-level only|
|Exact dates|Shifted by fixed offset|
|Organization names|Generalized|

---

## Key Findings Summary

| Metric | Value |
|--------|-------|
| Total Transactions Analyzed | 319 |
| Total Driver Earnings | INR 95,650.99 |
| Average Fare per Trip | INR 324.83 |
| Trip Completion Rate | 78.1% |
| Gini Coefficient (Earnings) | 0.2814 |
| Fare-Distance R² | 0.8968 |

### Fare Model

```markdown
Fare = 14.64 × Distance (km) + 73.50 (base fare)
R² = 0.8968 (89.68% variance explained)
```

### Fare Component Breakdown

- Base Fare: 89.2%
- Booking Fee: 7.5%
- Surge Pricing: 0.7%
- Other: 2.6%

---

## Running the Analysis

### Prerequisites

```bash
pip install pandas numpy scipy matplotlib seaborn
```

### Step 1: Anonymize Data (if using original data)

```bash
python code/anonymize_data.py
```

### Step 2: Run Analysis

```bash
python code/analysis.py
```

---

## Reproducibility

All statistics in the paper are derived from running `code/analysis.py` on the anonymized datasets. The analysis script outputs all values used in the paper.

---

## Citation

If you use this code or data in your research, please cite:

```bibtex
@inproceedings{author2026financial,
  title={A Financial Analytics Framework for Ride-Sharing Fleet Operations: An Empirical Study Using Real-World Transaction Data},
  author={[Author Name]},
  booktitle={Proceedings of the 5th International Conference on Nonlinear Dynamics and Applications (ICNDA)},
  year={2026},
  publisher={Springer}
}
```

---

## License

This project is for academic research purposes. The anonymized data may be used for non-commercial research with appropriate citation.

---

## Contact

[Add contact information]

---

## Acknowledgements

Data source: Real-world transaction reports from a commercial ride-sharing fleet operator (anonymized).
