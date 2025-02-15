import torch
import torch.nn as nn
import yaml

class FallbackMechanism(nn.Module):
    def __init__(self, input_size, output_size, hidden_size, num_layers, dropout):
        super(FallbackMechanism, self).__init__()
        self.input_pr = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size
        )

        with open('../config.yaml', 'r') as conf_file:
            conf = yaml.safe_load(conf_file)

        decoder_layer = nn.TransformerDecoderLayer(
            d_model=hidden_size,
            nhead=conf['nhead']
        )
        self.decoder = nn.TransformerDecoder(
            decoder_layer, num_layers
        )
        self.query = nn.Parameter(torch.randn(1, hidden_size))
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=-1)


    def forward(self, x):
        x = self.input_pr(x)
        x = x.transpose(0, 1)
        query = self.query.unsqueeze(1).expand(-1, x.size(1), -1)
        decoder_out = self.decoder(tgt=query, memory=x)
        decoder_out = decoder_out.squeeze(0)
        logits = self.fc(decoder_out)
        probabilities = self.softmax(logits)
        return probabilities
