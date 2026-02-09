Got it 👍 — **one single `README.md` file**, clean and proper.
Below is the **final version** you can paste **as-is** into `README.md`. Nothing else mixed in.

---

```markdown
# IoMT Network Anomaly Detection using Isolation Forest

This repository implements an **unsupervised anomaly detection framework** for
Internet of Medical Things (IoMT) network traffic using **Isolation Forest**.
The system is designed to support **micro-segmentation–based security monitoring**
by detecting abnormal behavior in allowed network flows.

---

## Problem Statement

IoMT networks consist of heterogeneous medical devices that generate complex and
highly variable network traffic. Traditional signature-based intrusion detection
systems struggle to detect **unknown or zero-day attacks** in such environments.

This project addresses the problem by:
- learning **normal IoMT network behavior** from benign traffic
- detecting deviations using **unsupervised machine learning**
- evaluating detection behavior across multiple real-world attack scenarios

---

## Approach

- **Learning paradigm**: Unsupervised learning  
- **Model**: Isolation Forest  
- **Training data**: Benign IoMT traffic only  
- **Evaluation data**: Multiple attack scenarios (DoS, DDoS, ARP spoofing, scans, MQTT attacks)  
- **Features**: Flow-level statistical and protocol features  
- **Labels**: Not used during training  

---

## Repository Structure

```

.
├── data_cleaning.py        # Cleans raw CSV files (numeric features, NaN/Inf handling)
├── scaling.py              # Fits and saves feature scaler using benign training data
├── train_iforest.py        # Trains Isolation Forest on scaled benign data
├── score_test_file.py      # Scores a single test file
├── automate_test.py        # Batch evaluation across all test files
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md

````

---

## Dataset

This project uses the **CIC IoMT dataset** available on Kaggle.

Due to **dataset size and licensing constraints**, the dataset and all derived
artifacts (cleaned CSVs, scaled data, trained models) are **not included** in
this repository.

The dataset must be downloaded separately and placed into appropriate
`train/` and `test/` directories.

---

## Setup

### Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
````

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Execution Pipeline

### 1. Data Cleaning

Cleans raw CSV files by keeping numeric features and removing invalid values.

```bash
python data_cleaning.py
```

---

### 2. Feature Scaling

Fits a `StandardScaler` using **benign training traffic only**.

```bash
python scaling.py
```

---

### 3. Model Training

Trains Isolation Forest on benign IoMT traffic.

```bash
python train_iforest.py
```

---

### 4. Evaluation

Runs anomaly detection across all test files.

```bash
python automate_test.py
```

Outputs include:

* anomaly counts
* anomaly fractions
* anomaly score statistics per attack type

---

## Model Configuration

* Algorithm: Isolation Forest
* Number of trees: 300
* Contamination: 0.02 (tuned using benign traffic to control false positives)
* Feature scaling: StandardScaler

---

## Key Observations

* Flooding and spoofing attacks generate strong anomaly signals
* Low-rate or protocol-conformant attacks are harder to detect
* Benign traffic exhibits limited false positives due to behavioral variability
* Results reflect realistic IoMT network behavior rather than inflated accuracy claims

---

## Micro-Segmentation Context

The anomaly detector is intended to operate **within micro-segmented IoMT network
zones**, where deviations in allowed communication behavior can indicate misuse
or compromise even when access control rules are satisfied.

---

## Notes

* This is an **unsupervised baseline**, not a signature-based IDS
* No attack labels are used during training
* The focus is on interpretability, realism, and reproducibility

---

## License

This repository is intended for academic and educational use.

Push it. You’re done with repo hygiene.
```
