import torch
import pandas as pd
import torch.nn.functional as F

def pad_to_k_and_mask(lst, k):
    padded_list = (lst + [-1] * k)[:k]
    mask = [1 if x >= 0 else 0 for x in padded_list]
    return padded_list, mask

def df_to_tensors(data_frame: pd.DataFrame, seq_len: int, node_count: int, k: int):
    # handling the case len(top_k) < k and creating a mask
    padded_data = data_frame.applymap(lambda x: pad_to_k_and_mask(x, k))
    padded_df = padded_data.applymap(lambda x: x[0])
    mask_df = padded_data.applymap(lambda x: x[1])

    # creating tensor to pass to the nn
    flattened_df = padded_df.applymap(lambda x: torch.tensor(x, dtype=torch.float32))
    flattened_df = flattened_df.values.flatten().tolist()
    input_tensor = torch.stack(flattened_df).view(-1, seq_len, node_count*k)
    # creating mask tensor
    flattened_mask = mask_df.applymap(lambda x: torch.tensor(x, dtype=torch.float32))
    flattened_mask = flattened_mask.values.flatten().tolist()
    mask_tensor = torch.stack(flattened_mask).view(-1, seq_len, node_count*k)
    return input_tensor, mask_tensor

def prepare_and_validate_tensor(data_frame, seq_len, node_count, k):
    data_frame = data_frame.drop(columns="timestamp")
    tensor, mask = df_to_tensors(data_frame, seq_len, node_count, k)
    return tensor, mask

def masked_loss(output, target, mask):
    loss = F.cross_entropy(output, target, reduction="none")
    mask_loss = loss * mask
    return mask_loss.sum() / mask.sum()
