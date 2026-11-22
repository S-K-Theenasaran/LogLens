
# LogLens

**Explainable Machine Learning for Server Log Anomaly Detection**

LogLens is a local Python application that analyzes server logs, groups similar messages using Drain3, and detects unusual activity using machine learning.

**Status:** Final submission preparation — November 22, 2026  
**Deadline:** November 23, 2026

## Technologies

- Python
- Pandas and NumPy
- Scikit-learn
- Drain3
- Streamlit
- SQLite (database initialization)

## Implemented Features

- Parse structured server logs and HDFS sample logs.
- Identify invalid log entries.
- Group similar messages using Drain3 template mining.
- Split logs chronologically into training and testing sets.
- Extract template-count features in five-minute windows.
- Count previously unseen log templates.
- Detect anomalies using Isolation Forest and LOF.
- Group nearby anomalous windows into incidents.
- Generate descriptive explanations for detected anomalies.
- Display model results through a local Streamlit dashboard.

## Installation

Clone the repository:

```powershell
git clone https://github.com/S-K-Theenasaran/LogLens.git
cd LogLens
git checkout feature/pipeline-integration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pandas numpy scikit-learn drain3 streamlit
```

## Running the Application

From the project root:

```powershell
$env:PYTHONPATH="src"
python -m streamlit run app.py
```

Open the local address displayed by Streamlit, usually:

http://localhost:8501

Upload a compatible server log file to run the anomaly detection pipeline.

## Supported Log Formats

### Structured logs

```text
2026-11-18 10:00:00 INFO Server User 123 logged in
2026-11-18 10:05:00 WARNING Database Connection slow
2026-11-18 10:10:00 ERROR Auth Invalid password
```

### HDFS logs

The application also supports the HDFS log format used by the Loghub HDFS sample.

The HDFS parser is selected for files whose paths contain `HDFS`.

## Machine Learning Pipeline

1. Parse log entries.
2. Split logs chronologically into training and testing sets.
3. Fit Drain3 templates using training logs.
4. Transform logs into template-count features.
5. Train Isolation Forest and Local Outlier Factor.
6. Detect anomalous test windows.
7. Group nearby anomalies into incidents.
8. Generate descriptive anomaly explanations.

Both models use the same training and testing feature sets.

## Synthetic Dataset Evaluation

The synthetic generator creates 50 five-minute windows with two deliberately injected high-volume anomalies.

The first 40 windows are used for training and the final 10 for testing.

### Results

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

Isolation Forest detected both injected anomalies without false positives.

LOF detected both anomalies but produced one false positive.

These results apply only to the small synthetic dataset and do not establish real-world model accuracy.

The evaluation results are stored in:

`docs/synthetic_evaluation.csv`

## Public HDFS Sample

LogLens was tested using the public `HDFS_2k.log` sample.

- Parsed log entries: 2,000
- Failed log entries: 0
- Training windows: 393
- Testing windows: 61
- Isolation Forest flagged windows: 7
- LOF flagged windows: 2

These are anomaly counts, not accuracy measurements.

The sample was processed using time windows. The full HDFS benchmark requires block-level evaluation with ground-truth labels.

## Testing

Activate the virtual environment and run:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

Additional standalone checks are available in the `tests` directory.

Generate synthetic logs with:

```powershell
python tests/generate_pipeline_logs.py
```

## Current Limitations

- Public-dataset precision, recall and F1 evaluation remains incomplete.
- HDFS is currently analyzed using time windows rather than block sessions.
- The current pipeline does not train exclusively on verified normal-labeled public logs.
- SQLite persistence is initialized but not fully integrated.
- The Streamlit dashboard is a functional prototype.
- Anomaly explanations describe feature deviations rather than proving root causes.

## Repository

https://github.com/S-K-Theenasaran/LogLens
