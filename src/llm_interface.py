import logging
import os
import re

import matplotlib.pyplot as plt
import openai
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.models.ml.lifter_dataset import IS_CLEAN_LABEL, IS_USING_LABEL
from src.result_subset import ResultSubset
from src.utils.known_ped_users import get_known_users
from src.utils.utils import POWERSTATS

logger = logging.getLogger(__name__)

load_dotenv(POWERSTATS / "openai_config.env")
API_KEY: str | None = os.getenv("API_KEY")
API_LOCAL_URL: str | None  = os.getenv("API_LOCAL_URL")
OPENAI_MODEL: str | None  = os.getenv("OPENAI_MODEL")

def dot_env_is_validish() -> bool:
    return OPENAI_MODEL is not None and (API_KEY is not None or API_LOCAL_URL is not None)

def summarize_data(results: list[ResultSubset]) -> None | str:
    if not dot_env_is_validish():
        logger.error("Please enter in the appropriate fields to 'powerstats/openai_config.env'")
        return None

    if not results:
        logger.warning("No results to summarize.")
        return None

    client = openai.OpenAI(api_key=API_KEY, base_url=API_LOCAL_URL)
    string_res = "\n".join([str(r) for r in results])
    prompt = f"""Given this sequence of data entries:\n{string_res}\n
Write a short analysis of the lifter's performance over time. Be concise but detailed in your summary.
Particularly, pay attention to if the lifter seems suspicious of drug use. Pay close attention to if both their
rate of performance seems too fast and if their absolute performance is too high. After analyzing the data,
give a likely hood on a scale 1-10 of how likely they are to be using performance enhancing drugs.
1/10 means very unlikely to be using drugs, 10/10 means almost certainly using drugs. Please add your rating like X/10.
That is, your response should look like:\nSummay here\nX/10"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions="You are a referee at a powerlifting competition responsible for selecting candidates for drug testing.",
        input=prompt,
        temperature=0.9
    )

    return str(response.output_text)

def get_rating(string: str) -> int:
    matches = re.findall(r'(\d{1,2})/10', string)
    if not matches:
        raise ValueError("No /10 rating found in string: " + string)
    return int(matches[-1])

def test_llm() -> None:
    if not dot_env_is_validish():
        logger.error("Please enter in the appropriate fields to 'powerstats/openai_config.env'")
        return None
    graph_loc = POWERSTATS / "graphs/llm"
    graph_loc.mkdir(exist_ok=True, parents=True)
    raw_output_dir = POWERSTATS / "llm_outputs"
    raw_output_dir.mkdir(exist_ok=True, parents=True)
    users = get_known_users()

    sequences = []
    labels = []
    for user, label in users:
        sequences.append(
            [ResultSubset.from_full_result(result) for result in user]
        )
        labels.append(label)
    pred = []
    labels_given_pred = []
    messups = 0
    for i, sequence in enumerate(sequences):
        response = summarize_data(sequence)
        if response is None:
            logger.error("Got a None response. Skipping data point")
            messups += 1
            continue
        try:
            rating = get_rating(response)
            if rating >= 6:
                pred.append(IS_USING_LABEL)
            else:
                pred.append(IS_CLEAN_LABEL)
            labels_given_pred.append(labels[i])
        except Exception as e:
            logger.error("Error getting rate. Not using data point in metrics", e)
            messups += 1
        (raw_output_dir / f"user_{i}_output_label_{labels[i]}.txt").write_text(f"{response}")
    if messups != 0:
        logger.warning("Got %s messups from LLM test", messups)
    metrics = {"accuracy": accuracy_score(labels_given_pred, pred),
            "precision": precision_score(labels_given_pred, pred, zero_division=0),
            "recall": recall_score(labels_given_pred, pred, zero_division=0),
            "f1": f1_score(labels_given_pred, pred, zero_division=0)}
    logger.info(
        "LLM %s evaluation on golden labels (%.2f%% labels were drug use = %s): %s",
        OPENAI_MODEL,
        len([lab for lab in labels_given_pred if lab == IS_USING_LABEL]) * 100 / len(labels_given_pred),
        IS_USING_LABEL,
        metrics,
    )

    # Filter metrics to plot (exclude tensors like predictions/labels)
    metrics_to_plot = {
        k.capitalize(): v for k, v in metrics.items() if isinstance(v, (float, int))
    }
    ordered_keys = ["F1", "Accuracy", "Precision", "Recall"]
    plot_metrics = {
        k: metrics_to_plot[k] for k in ordered_keys if k in metrics_to_plot
    }
    plt.figure(figsize=(8, 5))
    plt.bar(
        plot_metrics.keys(),
        plot_metrics.values(),
        color=["#4CAF50", "#2196F3", "#FFC107", "#FF5722"],
    )
    plt.ylim(0, 1.1)
    plt.title(f"LLM {OPENAI_MODEL} - Best Metric Scores on True Test Set")
    for i, (k, v) in enumerate(plot_metrics.items()):
        plt.text(i, v + 0.01, f"{v:.2f}", ha="center", va="bottom")
    plt.ylabel("Score")
    plt.xlabel(f"(Using drugs = class {IS_USING_LABEL})")
    plt.savefig(graph_loc / f"LLM_{re.sub(r'[^a-zA-Z0-9]', '', OPENAI_MODEL)}_test_metrics_bar.png") # type: ignore
    plt.close()
