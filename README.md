
# LogLens

**Explainable Machine Learning for Server Log Anomaly Detection**

LogLens is a local Python application that analyzes server logs, groups similar messages using Drain3, and detects unusual activity using machine learning.

**Status:** Final submission preparation — November 22, 2026  
**Submission deadline:** November 23, 2026

## Technologies

- Python 3
- Pandas and NumPy
- Scikit-learn
- Drain3
- Streamlit
- SQLite (database initialization)
- Pytest

The application runs machine learning models locally without external AI APIs.

## Implemented Features

- Parse structured server logs, HDFS, BGL, and OpenStack samples.
- Identify invalid log entries.
- Group similar messages using Drain3 template mining.
- Split logs chronologically into training and testing sets.
- Learn templates from training data only.
- Extract log-template counts within time windows.
- Extract severity-level counts (INFO, WARNING, ERROR, etc.).
- Count previously unseen log templates.
- Detect anomalies using Isolation Forest and Local Outlier Factor (LOF).
- Group nearby anomalous windows into incidents.
- Generate descriptive anomaly explanations.
- Display results through a local Streamlit dashboard.
- Compare model anomaly scores.

## Installation

Clone the repository:

```powershell
git clone https://github.com/S-K-Theenasaran/LogLens.git
cd LogLens

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install pandas numpy scikit-learn drain3 streamlit pytest
```

## Running the Application

From the project root:

```powershell
$env:PYTHONPATH = "src"
python -m streamlit run app.py
```

Open:

http://localhost:8501

Upload a compatible `.log` or `.txt` file to run anomaly detection.

## Supported Log Formats

### Structured logs

Example:

```text
2026-11-18 10:00:00 INFO Server User 123 logged in
2026-11-18 10:05:00 WARNING Database Connection slow
2026-11-18 10:10:00 ERROR Auth Invalid password
```

### Public dataset formats

- HDFS (`HDFS_2k.log`)
- BGL (`BGL_2k.log`)
- OpenStack (`OpenStack_2k.log`)

The pipeline currently selects specialized parsers based on recognizable filenames.

OpenStack uses one-minute windows, while HDFS and BGL use five-minute windows.

BGL processing avoids generating empty windows across sparse timestamps.

## Machine Learning Pipeline

1. Parse server log entries.
2. Split logs chronologically into training and testing datasets.
3. Learn Drain3 templates using training data only.
4. Apply learned templates to both datasets.
5. Extract template-count and severity-count features.
6. Train Isolation Forest and LOF.
7. Identify anomalous testing windows.
8. Group nearby anomalies into incidents.
9. Generate descriptive anomaly explanations.
10. Display results in Streamlit.

Both models use aligned training and testing feature sets.

## Synthetic Dataset Evaluation

An earlier synthetic evaluation used 50 five-minute windows with two deliberately injected high-volume anomalies.

The first 40 windows were used for training and the final 10 for testing.

### Recorded Results

| Metric | Isolation Forest | LOF |
|---|---:|---:|
| Test windows | 10 | 10 |
| True positives | 2 | 2 |
| False positives | 0 | 1 |
| False negatives | 0 | 0 |
| True negatives | 8 | 7 |
| Precision | 1.0000 | 0.6667 |
| Recall | 1.0000 | 1.0000 |
| F1 score | 1.0000 | 0.8000 |

These are previously recorded synthetic evaluation results and have not been revalidated following the latest feature-engineering changes.

The recorded results are stored in:

`docs/synthetic_evaluation.csv`

## Public Dataset Testing

The complete pipeline was successfully executed on three public log samples on November 22, 2026.

| Dataset | Training Windows | Testing Windows | Isolation Forest Anomalies | LOF Anomalies |
|---|---:|---:|---:|---:|
| HDFS | 393 | 61 | 8 | 1 |
| BGL | 664 | 167 | 0 | 8 |
| OpenStack | 12 | 3 | 0 | 0 |

These are predicted anomaly counts, not accuracy measurements.

Public dataset precision, recall, and F1 scores have not been established using ground-truth labels.

The OpenStack sample contains relatively few time windows and is primarily useful as a pipeline functionality check.

The full HDFS benchmark requires block-level evaluation with ground-truth labels, rather than only time-window anomaly counts.

## Testing

Activate the virtual environment and run:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests -v
```

Latest automated test results:

**7 passed — November 22, 2026**

Test coverage includes:

- Anomaly explanation
- Incident grouping
- Template counts
- Unknown templates
- Severity counts
- Empty time windows
- Missing-column validation

Additional standalone checks are available in the `tests` directory, including Isolation Forest, LOF, chronological splitting, and template mining.

## Streamlit Dashboard

The dashboard supports:

- Log file uploading
- Analyzed-window counts
- Isolation Forest anomaly counts
- LOF anomaly counts
- Model result tables
- Incident grouping
- Anomaly explanations
- Anomaly score visualization

The dashboard was verified successfully using the HDFS sample.

## Current Limitations

- Public dataset precision, recall, and F1 evaluation remains incomplete.
- HDFS is analyzed using time windows rather than block sessions.
- Training data is split chronologically but is not restricted to verified normal-labeled public logs.
- SQLite persistence is initialized but not fully integrated into the application.
- Parser selection currently depends on recognizable filenames.
- The dashboard is a functional local prototype.
- Anomaly explanations describe feature deviations rather than proving root causes.
- The synthetic evaluation has not been rerun following the latest feature-engineering changes.

## Repository

https://github.com/S-K-Theenasaran/LogLens
