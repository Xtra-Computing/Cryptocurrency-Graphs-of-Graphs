import torch
from torch_geometric.data import InMemoryDataset, DataLoader
import os

class TransactionDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(TransactionDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(os.path.join(self.root, 'processed', 'data.pt'))

    @property
    def processed_file_names(self):
        return ['data.pt']

    def get(self, idx):
        return self.get(idx)

    def len(self):
        return len(self.data.y)

    def get_label(self, idx):
        return self.data.y[idx].item()

