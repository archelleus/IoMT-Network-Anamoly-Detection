# IoMT Network Anomaly Detection

This repository contains machine learning pipelines designed to identify anomalies and cyberattacks in Internet of Medical Things (IoMT) network traffic. The system leverages both **Supervised** and **Unsupervised** machine learning approaches to ensure robust, highly accurate anomaly detection over high-dimensional networking metrics.

## Project Structure

- **`data_cleaning.py`**: A dedicated data engineering pipeline that loads extracted datasets and strictly scrubs duplicates, replaces infinite variables, handles nulls dynamically, and establishes normalized outputs.
- **`supervised_binary/`**: Supervised learning approach relying on `RandomForestClassifier`.
  - Formulates a generalized dataset balancing attacks (`1`) versus benign traffic (`0`).
  - Trains, scales, and persists the pipeline into lightweight artifacts.
  - Automatically assesses incoming traffic streams in `score_test_file.py`.
- **`unsupervised/`**: Unsupervised learning approach utilizing `IsolationForest`.
  - Assumes an unlabeled or heavily imbalanced environment.
  - Trained uniquely on scaled *benign* network traffic.
  - Establishes statistical bounds/thresholds dynamically. Points failing outside the boundary are marked as cyberattack anomalies.
- **`data/`**: Centralized storage mapping raw and cleaned train/test data appropriately. *(Note: specific network CSVs are `.gitignore`d locally to preserve space).*
- **`models/`**: Stores robust binary `.joblib` representations of trained machine learning components (e.g. Scikit-Learn pipelines, `rf_model`, `scaler`, `isolation_forest`).

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/archelleus/IoMT-Network-Anamoly-Detection.git
   cd IoMT-Network-Anamoly-Detection
   ```

2. **Create a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Restructure your freshly extracted IoMT PCAP/CSV captures into the `data/` directory. 
2. Process them comprehensively through the data cleaner: `python data_cleaning.py`.
3. To test the unsupervised framework locally: 
   ```bash
   cd unsupervised
   python automate_test.py
   ```
4. To run evaluation routines upon labeled binary attacks:
   ```bash
   cd supervised_binary
   python automate_test.py
   ```
