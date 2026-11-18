
# LogLens

**Explainable Machine Learning for Server Log Anomaly Detection**

LogLens is a Python-based application for detecting unusual activity in server logs using machine learning.

**Project Status:** Working Draft — November 18, 2026  
**Final Submission Deadline:** November 23, 2026

## Technologies

- Python
- Pandas and NumPy
- Scikit-learn
- Drain3
- Streamlit
- SQLite (database initialization implemented)

## Implemented Features

- Parse structured server logs and identify invalid entries.
- Group similar log messages using Drain3.
- Split training and testing logs chronologically.
- Extract log-template counts in five-minute windows.
- Detect anomalies using Isolation Forest.
- Detect anomalies using Local Outlier Factor (LOF).
- Display anomaly results in a local Streamlit dashboard.
- Upload log files and compare model outputs.

## Installation

Clone the repository:

```bash
git clone https://github.com/S-K-Theenasaran/LogLens.git
cd LogLens
git checkout feature/pipeline-integration
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install pandas numpy scikit-learn drain3 streamlit
```

## Running LogLens

From the project root, run:

```powershell
$env:PYTHONPATH="src"
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

Upload a compatible server log file to analyze its activity.

### Supported Log Format

The current parser expects structured log entries such as:

```text
2026-11-18 10:00:00 INFO Server User 123 logged in
2026-11-18 10:05:00 WARNING Database Connection slow
2026-11-18 10:10:00 ERROR Auth Invalid password
```

The current pipeline requires at least three training time windows and a separate testing window.

## Testing

Generate synthetic server logs:

```powershell
python tests/generate_pipeline_logs.py
```

The generator creates `data/pipeline_test.log`, containing normal activity and two deliberately injected activity spikes.

Upload this file through the Streamlit dashboard.

### Initial Synthetic Test Results

| Model | Anomalous Windows |
|---|---:|
| Isolation Forest | 2 |
| Local Outlier Factor | 3 |

Both models flagged the two injected activity spikes.

These results demonstrate that the prototype runs on synthetic data. They do not establish accuracy on real-world server logs.

## Current Limitations

- Unseen log templates are not yet represented by a dedicated feature.
- Model evaluation on public datasets is pending.
- Incident grouping is not yet implemented.
- Detailed anomaly explanations are not yet implemented.
- The dashboard is an initial prototype.
- SQLite persistence is not yet integrated into the analysis pipeline.

## Planned Work Before Final Submission

1. Evaluate both models using public log datasets.
2. Calculate precision, recall and F1-score where ground-truth labels are available.
3. Implement incident grouping.
4. Improve anomaly explainability.
5. Enhance the dashboard.
6. Complete documentation, testing and demonstration materials.

## Project Repository

https://github.com/S-K-Theenasaran/LogLens

**Current Working Branch:** `feature/pipeline-integration`
