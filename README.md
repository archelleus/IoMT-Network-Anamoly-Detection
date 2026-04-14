Alright — here is the **entire README as plain text (no code block, no truncation, no formatting issues)**. Just copy everything below:

---

# IoMT Network Anomaly Detection

This repository contains machine learning pipelines designed to identify anomalies and cyberattacks in Internet of Medical Things (IoMT) network traffic. The system leverages both **Supervised** and **Unsupervised** machine learning approaches to ensure robust, highly accurate anomaly detection over high-dimensional networking metrics.

---

## Project Structure

* **`data_cleaning.py`**: A dedicated data engineering pipeline that loads extracted datasets and strictly scrubs duplicates, replaces infinite variables, handles nulls dynamically, and establishes normalized outputs.
* **`supervised_binary/`**: Supervised learning approach relying on `RandomForestClassifier`.

  * Formulates a generalized dataset balancing attacks (`1`) versus benign traffic (`0`).
  * Trains, scales, and persists the pipeline into lightweight artifacts.
  * Automatically assesses incoming traffic streams in `score_test_file.py`.
* **`unsupervised/`**: Unsupervised learning approach utilizing `IsolationForest`.

  * Assumes an unlabeled or heavily imbalanced environment.
  * Trained uniquely on scaled *benign* network traffic.
  * Establishes statistical bounds/thresholds dynamically. Points failing outside the boundary are marked as cyberattack anomalies.
* **`data/`**: Centralized storage mapping raw and cleaned train/test data appropriately. *(Note: specific network CSVs are `.gitignore`d locally to preserve space).*
* **`models/`**: Stores robust binary `.joblib` representations of trained machine learning components (e.g. Scikit-Learn pipelines, `rf_model`, `scaler`, `isolation_forest`).

---

## Setup Instructions

1. Clone the repository:
   git clone [https://github.com/archelleus/IoMT-Network-Anamoly-Detection.git](https://github.com/archelleus/IoMT-Network-Anamoly-Detection.git)
   cd IoMT-Network-Anamoly-Detection

2. Create a virtual environment (Optional but Recommended):
   python -m venv venv
   source venv/bin/activate   (On Windows: venv\Scripts\activate)

3. Install the required packages:
   pip install -r requirements.txt

---

## Usage

1. Restructure your freshly extracted IoMT PCAP/CSV captures into the `data/` directory.

2. Process them through the data cleaner:
   python data_cleaning.py

3. To test the unsupervised framework:
   cd unsupervised
   python automate_test.py

4. To evaluate labeled binary attacks:
   cd supervised_binary
   python automate_test.py

---

## Comparative Results

| Attack Type          | Binary RF (Attack Fraction) | Multiclass RF (Dominant Confidence) | Isolation Forest (Mean Score)    |
| -------------------- | --------------------------- | ----------------------------------- | -------------------------------- |
| Benign               | 0.00 (Correct)              | High (Class 0)                      | ~0.20 (Most Normal)              |
| DDoS (UDP/TCP)       | ~1.00                       | Very High                           | ~0.004 – 0.01 (Highly Anomalous) |
| DoS (TCP/UDP/SYN)    | ~1.00                       | Very High                           | ~0.01 – 0.05                     |
| MQTT DoS             | ~1.00                       | Very High                           | ~0.18 (Near Normal)              |
| Recon (Port/OS Scan) | 0.90 – 0.97                 | High                                | ~0.05 – 0.10                     |
| ARP Spoofing         | ~0.65                       | Moderate (Mixed)                    | ~0.10 – 0.15                     |
| Vulnerability Scan   | ~0.39                       | Low (Mixed)                         | ~0.15 – 0.16                     |

---

## Key Observations

Binary Random Forest:

* Near-perfect detection for high-volume attacks (DDoS/DoS)
* Performance drops for subtle attacks (VulScan, ARP)
* Strong separation between benign and malicious traffic

Multiclass Random Forest:

* High-confidence classification for major attack categories
* Some overlap between similar or weak attack types
* Useful for attack identification rather than just detection

Isolation Forest:

* Clear distinction between normal and anomalous traffic
* Highly effective for extreme/volumetric attacks
* Less effective for attacks that resemble normal behavior

---

## Conclusion

This project evaluates multiple machine learning approaches for IoMT intrusion detection rather than relying on a single model.

* Supervised models (Random Forest) perform exceptionally well when attack patterns are known and represented in training data
* Unsupervised methods (Isolation Forest) detect behavioral anomalies but struggle with subtle or near-normal attack patterns

Key takeaway:
No single approach performs optimally across all attack types.

* High-intensity attacks are consistently detected across models
* Low-intensity or stealth attacks remain challenging
* Some attacks closely resemble normal traffic, limiting detection capability

Overall, the results show that different approaches provide complementary insights:

* Binary RF → strongest for detection
* Multiclass RF → strongest for classification
* Isolation Forest → strongest for anomaly discovery

This work provides a solid foundation for developing more robust and adaptive IoMT intrusion detection systems.

---

## Limitations

* Binary model may overfit dataset-specific patterns
* Isolation Forest struggles with stealth attacks
* No cross-dataset validation performed yet

---

## Future Work

* Evaluate on additional datasets
* Improve detection of low-signal attacks
* Apply feature engineering and selection
* Build visualization/dashboard for analysis

---

## Author

Bhavya Jain

---

## License

This project is intended for academic and research purposes.
