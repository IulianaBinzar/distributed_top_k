import torch.nn as nn
import torch
import pandas as pd
import logging


def df_to_tensor(data_frame: pd.DataFrame, seq_len: int, node_count: int, k: int):
    flattened_df = data_frame.applymap(lambda x: torch.tensor(x, dtype=torch.float32))
    flattened_df = flattened_df.values.flatten().tolist()
    input_tensor = torch.stack(flattened_df).view(-1, seq_len, node_count*k)
    return input_tensor

class FallbackMechanism(nn.Module):
    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
        super(FallbackMechanism, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size,
                            hidden_size=hidden_size,
                            num_layers=num_layers,
                            dropout=dropout
                            )
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=-1)

    def feed_data(self, data_frame, seq_len, node_count, k):
        data_frame = data_frame.drop(columns="timestamp")
        tensor = df_to_tensor(data_frame, seq_len, node_count, k)
        self.forward(tensor)
        pass

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden_state = lstm_out[:, -1, :]
        logits = self.fc(last_hidden_state)
        probabilities = self.softmax(logits)
        return probabilities

