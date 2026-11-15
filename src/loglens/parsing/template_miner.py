import pandas as pd
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig


def mine_log_templates(logs: pd.DataFrame) -> pd.DataFrame:
    """Mine log templates and assign the final template to each message."""

    if "message" not in logs.columns:
        raise ValueError("Input logs must contain a 'message' column.")

    config = TemplateMinerConfig()
    config.profiling_enabled = False

    miner = TemplateMiner(config=config)
    results = logs.copy()

    cluster_ids = []

    for message in results["message"]:
        if pd.isna(message):
            cluster_ids.append(None)
            continue

        mined = miner.add_log_message(str(message))
        cluster_ids.append(mined["cluster_id"])

    results["template_id"] = cluster_ids

    # Retrieve the final templates after processing all messages.
    final_templates = {
        cluster.cluster_id: cluster.get_template()
        for cluster in miner.drain.clusters
    }

    results["template"] = results["template_id"].map(final_templates)

    return results
