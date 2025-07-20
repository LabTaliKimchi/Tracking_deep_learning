import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import random

class SyntheticMotifDataset(Dataset):
    def __init__(self, num_samples=500, seq_len=1024, num_motifs=5):
        self.data = []
        self.labels = []
        motifs = [np.sin(np.linspace(0, np.pi, 50) + np.random.rand()) * (i + 1)
                  for i in range(num_motifs)]
        for _ in range(num_samples):
            signal = np.zeros(seq_len)
            label = np.zeros(seq_len, dtype=int)
            pos = 0
            while pos < seq_len - 60:
                idx = random.randint(0, num_motifs - 1)
                motif = motifs[idx]
                l = len(motif)
                signal[pos:pos+l] += motif
                label[pos:pos+l] = idx + 1
                pos += l + random.randint(5, 20)
            self.data.append(signal)
            self.labels.append(label)
            a=1

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = torch.tensor(self.data[idx], dtype=torch.float32).unsqueeze(0)
        y = torch.tensor(self.labels[idx], dtype=torch.int64)
        return x, y

class TweetyNet1D(nn.Module):
    def __init__(self, n_classes, input_channels=1):
        super().__init__()
        self.conv1 = nn.Conv1d(input_channels, 32, 5, padding=2)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(32, 64, 5, padding=2)
        self.pool2 = nn.MaxPool1d(2)
        self.lstm = nn.LSTM(64, 128, batch_first=True, bidirectional=True)
        self.classifier = nn.Linear(256, n_classes)

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = x.permute(0, 2, 1)
        x, _ = self.lstm(x)
        return self.classifier(x)

def train(model, loader, criterion, optimizer, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for x, y in loader:
            optimizer.zero_grad()
            out = model(x)
            y_ds = y[:, ::4]
            loss = criterion(out.view(-1, out.shape[-1]), y_ds.view(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {total_loss / len(loader):.4f}")

if __name__ == "__main__":
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)

    dataset = SyntheticMotifDataset()
    loader = DataLoader(dataset, batch_size=16, shuffle=True)
    model = TweetyNet1D(n_classes=6)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    train(model, loader, criterion, optimizer)
    print("Training complete.")

