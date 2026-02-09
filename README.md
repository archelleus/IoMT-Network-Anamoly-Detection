# IoMT Network Anomaly Detection (Isolation Forest)

Unsupervised anomaly detection for **Internet of Medical Things (IoMT)** network traffic using **Isolation Forest**, designed to support **micro-segmentation–based security monitoring**.

This project learns *normal network behavior* from benign traffic and detects deviations without relying on attack labels.

---

## Why this project?

IoMT networks are:
- highly heterogeneous  
- noisy and dynamic  
- vulnerable to unknown / zero-day attacks  

Signature-based intrusion detection systems struggle in such environments.

**This project uses unsupervised learning** to detect anomalous behavior directly from network flow statistics.

---

## Core Idea

- Train on **benign IoMT traffic only**
- Learn what *normal* looks like
- Flag traffic that deviates from learned behavior
- No attack labels used during training

---

## Approach

- **Learning type**: Unsupervised  
- **Model**: Isolation Forest  
- **Features**: Flow-level statistical & protocol features  
- **Training data**: Benign traffic only  
- **Evaluation data**: Multiple attack scenarios (DoS, DDoS, ARP spoofing, scans, MQTT attacks)

---

## Repository Structure

```
.
├── data_cleaning.py        # Cleans raw CSV files
├── scaling.py              # Feature scaling (benign data only)
├── train_iforest.py        # Train Isolation Forest
├── score_test_file.py      # Score a single test file
├── automate_test.py        # Batch evaluation on all test files
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Dataset

- **Dataset**: CIC IoMT (Kaggle)
- The dataset and derived files are **NOT included** due to size and licensing constraints.

Download the dataset separately and place files into appropriate `train/` and `test/` directories.

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## How to Run

### 1. Clean data
```bash
python data_cleaning.py
```

### 2. Scale benign training data
```bash
python scaling.py
```

### 3. Train the model
```bash
python train_iforest.py
```

### 4. Evaluate on test data
```bash
python automate_test.py
```

Evaluation outputs:
- anomaly counts
- anomaly fractions
- anomaly score statistics per attack type

---

## Model Configuration

- **Algorithm**: Isolation Forest  
- **Trees**: 300  
- **Contamination**: 0.02  
- **Scaler**: StandardScaler  

---

## Observations

- Flooding and spoofing attacks are strongly detected
- Low-rate or protocol-conformant attacks are harder to detect
- Benign traffic shows limited false positives
- Results reflect realistic IoMT network behavior

---

## Micro-Segmentation Context

The anomaly detector is intended to operate **inside micro-segmented IoMT zones**, where:
- access control restricts communication paths
- anomaly detection identifies misuse of allowed flows

---

## Notes

- Unsupervised baseline (not signature-based IDS)
- No attack labels used during training
- Focus on realism and reproducibility

---

## License

For academic and educational use only.
