import torch
import pandas as pd
import numpy as np
import torch.nn.functional as F


def pad_to_k_and_mask(lst, k):
    padded_list = (lst + [-1] * k)[:k]
    mask = [1 if x >= 0 else 0 for x in padded_list]
    return padded_list, mask


def df_to_tensors(data_frame: pd.DataFrame, seq_len: int, node_count: int, k: int):
    # handling the case len(top_k) < k and creating a mask
    padded_data = {
        col: data_frame[col].map(lambda x: pad_to_k_and_mask(x, k))
        for col in data_frame.columns
    }
    padded_df = pd.DataFrame(
        {col: padded_data[col].map(lambda x: x[0]) for col in padded_data}
    )
    mask_df = pd.DataFrame(
        {col: padded_data[col].map(lambda x: x[1]) for col in padded_data}
    )

    # creating tensor to pass to the nn
    flattened_df = pd.DataFrame(
        {
            col: padded_df[col].map(lambda x: torch.tensor(x, dtype=torch.float32))
            for col in padded_df
        }
    )
    flattened_df = flattened_df.values.flatten().tolist()
    input_tensor = torch.stack(flattened_df).view(-1, seq_len, node_count * k)
    # creating mask tensor
    flattened_mask = pd.DataFrame(
        {
            col: mask_df[col].map(lambda x: torch.tensor(x, dtype=torch.float32))
            for col in mask_df
        }
    )
    flattened_mask = flattened_mask.values.flatten().tolist()
    mask_tensor = torch.stack(flattened_mask).view(-1, seq_len, node_count * k)
    return input_tensor, mask_tensor


def masked_loss(output, target, mask):
    loss = F.cross_entropy(output, target, reduction="none")
    mask_loss = loss * mask
    return mask_loss.sum() / mask.sum()


# The functions below were taken from ChatGPT
def evaluate_top_k(predicted, ground_truth, k):
    f1_score = f1_score_at_k(predicted, ground_truth, k)
    pos_score = position_score(predicted, ground_truth, k)
    ndcg = ndcg_at_k(predicted, ground_truth, k)
    return precision, pos_score, ndcg


def dcg_at_k(predicted, ground_truth, k):
    dcg = 0
    for i, pred_item in enumerate(predicted[:k]):
        if pred_item in ground_truth:
            dcg += 1 / np.log2(i + 2)  # Log base-2 discount
    return dcg


def ndcg_at_k(predicted, ground_truth, k):
    dcg = dcg_at_k(predicted, ground_truth, k)
    ideal_dcg = dcg_at_k(ground_truth, ground_truth, k)
    return dcg / ideal_dcg if ideal_dcg > 0 else 0


def f1_score_at_k(predicted, ground_truth, k):
    predicted_set = set(predicted[:k])
    ground_truth_set = set(ground_truth[:k])

    intersection = len(predicted_set & ground_truth_set)

    precision = intersection / k
    recall = intersection / len(ground_truth_set)

    if precision + recall == 0:
        return 0.0
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score
