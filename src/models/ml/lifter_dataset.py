import logging
from typing import Sequence

import torch
from torch import Tensor
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset

from src.database.database import Database
from src.database.tables.dto_table.lifter import LifterTable
from src.database.tables.dto_table.result import ResultTable
from src.models.dto.lifter import Lifter
from src.models.dto.result import Result

logger = logging.getLogger(__name__)


class LifterDataset(Dataset[tuple[Tensor, float]]): # type: ignore
    def __init__(self, sequences: list[Tensor], labels: list[float]) -> None:
        self.sequences: list[Tensor] = sequences
        self.labels: list[float] = labels

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> tuple[Tensor, float]:
        return self.sequences[idx], self.labels[idx]


def collate_fn(
    batch: Sequence[tuple[Tensor, float]],
) -> tuple[Tensor, Tensor]:
    sequences, labels = zip(*batch)
    padded_seqs: Tensor = pad_sequence(sequences, batch_first=True)
    label_tensor: Tensor = torch.tensor(labels, dtype=torch.float32)
    return padded_seqs, label_tensor


def is_valid_result(result: Result) -> bool:
    return (
        result.total_kg is not None
        and result.total_kg > 0
        and result.event == "SBD"
        and result.equipment == "Raw"
        and result.age is not None
        and result.bodyweight_kg is not None
        and result.best3_bench_kg is not None
        and result.best3_bench_kg > 0
        and result.best3_squat_kg is not None
        and result.best3_squat_kg > 0
        and result.best3_deadlift_kg is not None
        and result.best3_deadlift_kg > 0
    )


def get_train_test_data_from_extracted(
    data: list[tuple[list[Result], Lifter]],
) -> tuple[DataLoader, DataLoader]:
    sequences = []
    labels = []
    for list_results, lifter in data:
        for i in range(len(list_results)):
            new_sequence = []
            for j in range(i + 1):
                result = list_results[j]
                new_sequence.append(
                    [
                        result.best3_bench_kg,
                        result.best3_deadlift_kg,
                        result.best3_squat_kg,
                        result.total_kg,
                        result.bodyweight_kg,
                        result.age,
                        1 if lifter.sex == "M" else 0,
                    ]
                )
            sequences.append(torch.tensor(new_sequence, dtype=torch.float32))
            labels.append(1.0 if list_results[i].tested else 0.0)
    logger.info(
        "Created %d sequences from %d result entries", len(sequences), len(data)
    )
    dataset = LifterDataset(sequences, labels)
    train, test = torch.utils.data.random_split(dataset, [0.8, 0.2])
    logger.info(
        "Training dataset size: %d Testing dataset size: %d", len(train), len(test)
    )
    return DataLoader(
        train, shuffle=True, batch_size=128, collate_fn=collate_fn
    ), DataLoader(test, collate_fn=collate_fn)


def get_train_test_data_from_db() -> tuple[DataLoader, DataLoader]:
    database = Database()
    result_table = ResultTable(database)
    lifter_table = LifterTable(database)
    all_results = result_table.get_all()

    all_results = list(filter(lambda res: is_valid_result(res), all_results))
    all_lifters = lifter_table.get_all()

    lifter_id_to_result_and_lifter: dict[int, tuple[list[Result], Lifter]] = {}
    for lifter in all_lifters:
        if lifter.sex == "Mx":
            continue
        lifter_id_to_result_and_lifter[lifter.lifter_id] = ([], lifter)
    for result in all_results:
        if result.lifter_id in lifter_id_to_result_and_lifter:
            lifter_id_to_result_and_lifter[result.lifter_id][0].append(result)
    return get_train_test_data_from_extracted(
        [
            (res, lifter)
            for res, lifter in lifter_id_to_result_and_lifter.values()
            if len(res) > 0
        ]
    )
