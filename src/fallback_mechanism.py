import torch.nn as nn


class FallbackMechanism(nn.Module):
    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
        super(FallbackMechanism, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
        )
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden_state = lstm_out[:, -1, :]
        logits = self.fc(last_hidden_state)
        probabilities = self.softmax(logits)
        return probabilities
