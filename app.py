
import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path

from loglens.pipeline import run_pipeline


st.set_page_config(
    page_title="LogLens",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 LogLens")
st.subheader("Explainable ML for Server Log Anomaly Detection")

st.write(
    "Upload a server log file to detect unusual activity "
    "using Isolation Forest and Local Outlier Factor."
)

uploaded_file = st.file_uploader(
    "Upload a server log file",
    type=["log", "txt"],
)

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "uploaded.log"
        file_path.write_bytes(uploaded_file.getvalue())

        try:
            with st.spinner("Analyzing server logs..."):
                results = run_pipeline(str(file_path))

            isolation_results = results["isolation_results"]
            lof_results = results["lof_results"]

            st.success("Log analysis completed!")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Analyzed Windows",
                len(results["test_features"]),
            )

            col2.metric(
                "Isolation Forest Anomalies",
                int(isolation_results["is_anomaly"].sum()),
            )

            col3.metric(
                "LOF Anomalies",
                int(lof_results["is_anomaly"].sum()),
            )

            st.subheader("Isolation Forest Results")
            st.dataframe(
                isolation_results,
                use_container_width=True,
            )

            st.subheader("Local Outlier Factor Results")
            st.dataframe(
                lof_results,
                use_container_width=True,
            )

           

            st.subheader("Detected Incidents")

            st.write("Isolation Forest Incidents")
            st.dataframe(
                results["isolation_incidents"],
                use_container_width=True,
            )

            st.write("Local Outlier Factor Incidents")
            st.dataframe(
                results["lof_incidents"],
                use_container_width=True,
            )

            st.subheader("Anomaly Explanations")

            st.write("Isolation Forest Explanations")
            st.dataframe(
                results["isolation_explanations"],
                use_container_width=True,
            )

            st.write("Local Outlier Factor Explanations")
            st.dataframe(
                results["lof_explanations"],
                use_container_width=True,
            )

            st.caption(
                "Explanations show differences from training averages, "
                "not the exact causes of model predictions."
            )
            

            st.subheader("Anomaly Score Comparison")

            comparison = pd.DataFrame({
                "Isolation Forest": isolation_results["anomaly_score"],
                "LOF": lof_results["anomaly_score"],
            })

            st.line_chart(comparison)

            st.info(
                "Model scores have different scales and "
                "should not be compared by absolute magnitude."
            )

        except Exception as error:
            st.error(f"Analysis failed: {error}")
